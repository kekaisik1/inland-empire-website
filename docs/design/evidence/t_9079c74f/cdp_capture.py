#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:8057'
PORT = 9227
CHROME = os.environ.get('CHROME_BIN', 'google-chrome')

ROUTES = [
    ('home-en', '/'),
    ('services-en', '/services/'),
    ('service-refrigerator-en', '/services/refrigerator-repair/'),
    ('areas-en', '/service-areas/'),
    ('city-corona-en', '/service-areas/appliance-repair-corona-ca/'),
    ('blog-en', '/blog/'),
    ('contact-en', '/contact/'),
    ('search-en', '/search/?q=washer'),
    ('home-es', '/es/'),
    ('services-es', '/es/services/'),
    ('service-refrigerator-es', '/es/services/refrigerator-repair/'),
    ('city-corona-es', '/es/service-areas/appliance-repair-corona-ca/'),
    ('blog-es', '/es/blog/'),
]
VIEWPORTS = [
    ('desktop-1440x900', 1440, 900),
    ('laptop-1280x720', 1280, 720),
    ('tablet-768x1024', 768, 1024),
    ('mobile-390x844', 390, 844),
    ('small-mobile-360x740', 360, 740),
]
SCREENSHOT_COMBOS = set()  # screenshots are captured separately with Chrome CLI
SCREENSHOT_PLAN = {
    ('home-en', 'desktop-1440x900'), ('home-en', 'mobile-390x844'), ('home-en', 'tablet-768x1024'),
    ('services-en', 'desktop-1440x900'), ('service-refrigerator-en', 'desktop-1440x900'), ('service-refrigerator-en', 'mobile-390x844'),
    ('areas-en', 'desktop-1440x900'), ('city-corona-en', 'desktop-1440x900'), ('city-corona-en', 'mobile-390x844'),
    ('blog-en', 'desktop-1440x900'), ('contact-en', 'desktop-1440x900'), ('search-en', 'desktop-1440x900'),
    ('home-es', 'desktop-1440x900'), ('home-es', 'mobile-390x844'), ('service-refrigerator-es', 'mobile-390x844'), ('city-corona-es', 'desktop-1440x900'), ('blog-es', 'desktop-1440x900'),
}

def ws_connect(ws_url: str) -> socket.socket:
    u = urlparse(ws_url)
    s = socket.create_connection((u.hostname, u.port), timeout=10)
    key = base64.b64encode(os.urandom(16)).decode()
    target = u.path + (f'?{u.query}' if u.query else '')
    req = (f'GET {target} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n')
    s.sendall(req.encode())
    resp = b''
    while b'\r\n\r\n' not in resp:
        resp += s.recv(4096)
    if b' 101 ' not in resp.split(b'\r\n', 1)[0]:
        raise RuntimeError(resp[:200])
    return s

def ws_send(s: socket.socket, payload: dict) -> None:
    data = json.dumps(payload).encode()
    header = bytearray([0x81])
    n = len(data)
    if n < 126:
        header.append(0x80 | n)
    elif n < 65536:
        header.append(0x80 | 126); header.extend(struct.pack('!H', n))
    else:
        header.append(0x80 | 127); header.extend(struct.pack('!Q', n))
    mask = os.urandom(4)
    header.extend(mask)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    s.sendall(header + masked)

def recvn(s: socket.socket, n: int) -> bytes:
    out = b''
    while len(out) < n:
        chunk = s.recv(n - len(out))
        if not chunk:
            raise EOFError('socket closed')
        out += chunk
    return out

def ws_recv(s: socket.socket) -> dict:
    b1, b2 = recvn(s, 2)
    ln = b2 & 0x7f
    if ln == 126:
        ln = struct.unpack('!H', recvn(s, 2))[0]
    elif ln == 127:
        ln = struct.unpack('!Q', recvn(s, 8))[0]
    if b2 & 0x80:
        mask = recvn(s, 4)
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(recvn(s, ln)))
    else:
        data = recvn(s, ln)
    if (b1 & 0x0f) == 8:
        raise EOFError('websocket closed')
    return json.loads(data.decode())

class CDP:
    def __init__(self, sock: socket.socket):
        self.s = sock; self.i = 0; self.events = []
    def call(self, method: str, params: dict | None = None, timeout: float = 15):
        self.i += 1
        mid = self.i
        ws_send(self.s, {'id': mid, 'method': method, 'params': params or {}})
        end = time.time() + timeout
        while time.time() < end:
            self.s.settimeout(max(0.1, end - time.time()))
            try:
                msg = ws_recv(self.s)
            except socket.timeout:
                continue
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})
            self.events.append(msg)
        raise TimeoutError(method)
    def drain(self, seconds: float = 0.5):
        end = time.time() + seconds
        while time.time() < end:
            try:
                self.s.settimeout(max(0.05, end - time.time()))
                self.events.append(ws_recv(self.s))
            except Exception:
                break

def wait_http():
    for _ in range(50):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=0.2).read()
            return
        except Exception:
            time.sleep(0.1)
    raise RuntimeError('Chrome CDP did not start')

profile = tempfile.mkdtemp(prefix='ie-cdp-')
proc = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PORT}', f'--user-data-dir={profile}', '--disable-gpu', '--no-first-run', '--no-default-browser-check', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    wait_http()
    targets = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/list'))
    page_targets = [t for t in targets if t.get('type') == 'page']
    ws = page_targets[0]['webSocketDebuggerUrl']
    c = CDP(ws_connect(ws))
    for m in ['Page.enable', 'Runtime.enable', 'Log.enable', 'Network.enable', 'Accessibility.enable']:
        c.call(m)
    results = []
    for vp_name, w, h in VIEWPORTS:
        c.call('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': 1, 'mobile': w < 800})
        for route_name, path in ROUTES:
            c.events.clear()
            url = BASE + path
            c.call('Page.navigate', {'url': url}, timeout=10)
            for _ in range(20):
                time.sleep(0.1)
                c.drain(0.02)
                try:
                    state = c.call('Runtime.evaluate', {'expression': 'document.readyState', 'returnByValue': True}, timeout=1)['result'].get('value')
                    if state == 'complete':
                        break
                except Exception:
                    pass
            c.drain(0.1)
            expr = r'''(() => {
  const visible = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && Number(cs.opacity || 1) !== 0; };
  const nameOf = el => (el.getAttribute('aria-label') || el.getAttribute('title') || el.innerText || Array.from(el.querySelectorAll('img[alt]')).map(i=>i.alt).join(' ') || '').trim();
  const controls = Array.from(document.querySelectorAll('a,button,input,select,textarea,[role="button"],[role="link"]')).filter(visible);
  const smallTargets = controls.filter(el => { const r = el.getBoundingClientRect(); return r.width < 44 || r.height < 44; }).map(el => ({tag: el.tagName, text: nameOf(el).slice(0,60), w: Math.round(el.getBoundingClientRect().width), h: Math.round(el.getBoundingClientRect().height)}));
  const unnamed = controls.filter(el => !nameOf(el)).map(el => el.outerHTML.slice(0,120));
  const mobileToggle = document.querySelector('button[aria-controls="mobile-menu"]');
  const bg = getComputedStyle(document.body).backgroundColor;
  const primary = getComputedStyle(document.documentElement).getPropertyValue('--color-primary') || getComputedStyle(document.documentElement).getPropertyValue('--accent-yellow');
  return {url: location.href, title: document.title, lang: document.documentElement.lang, h1: Array.from(document.querySelectorAll('h1')).map(h=>h.innerText.trim()).slice(0,3), bg, primary: primary.trim(), scrollWidth: document.documentElement.scrollWidth, innerWidth, horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1, controls: controls.length, smallTargets: smallTargets.slice(0,12), unnamedControls: unnamed.slice(0,8), missingImages: Array.from(document.images).filter(i => !i.complete || i.naturalWidth === 0).map(i=>i.currentSrc || i.src).slice(0,8), hasMain: !!document.querySelector('main'), hasNav: !!document.querySelector('nav'), hasFooter: !!document.querySelector('footer'), mobileToggleAria: mobileToggle ? mobileToggle.getAttribute('aria-expanded') : null, bodyMentionsLOWL: document.body.innerText.includes('LOWL'), bookingLinks: Array.from(document.querySelectorAll('[data-booking]')).map(a=>a.href).slice(0,3)};
})()'''
            obs = c.call('Runtime.evaluate', {'expression': expr, 'returnByValue': True}, timeout=10)['result'].get('value')
            page_errors = [e for e in c.events if e.get('method') in ('Runtime.exceptionThrown', 'Log.entryAdded', 'Network.loadingFailed')]
            entry = {'route': route_name, 'path': path, 'viewport': vp_name, 'width': w, 'height': h, 'observations': obs, 'event_count': len(c.events), 'errors': page_errors[:10]}
            if (route_name, vp_name) in SCREENSHOT_COMBOS:
                entry['screenshot'] = f'{vp_name}__{route_name}.png'
            if w < 800 and route_name in ('home-en', 'home-es'):
                c.call('Runtime.evaluate', {'expression': "document.querySelector('button[aria-controls=\\\"mobile-menu\\\"]')?.click()", 'returnByValue': True})
                time.sleep(0.3)
                state = c.call('Runtime.evaluate', {'expression': "(() => { const b=document.querySelector('button[aria-controls=\\\"mobile-menu\\\"]'); const m=document.querySelector('#mobile-menu'); return {expanded:b?.getAttribute('aria-expanded'), menuVisible: !!m && getComputedStyle(m).display !== 'none' && m.getBoundingClientRect().height > 0}; })()", 'returnByValue': True})['result'].get('value')
                entry['mobile_menu_after_click'] = state
                fn = f'{vp_name}__{route_name}__mobile-menu-open.png'
                entry['mobile_menu_screenshot'] = fn
            results.append(entry)
    (ROOT / 'browser-observations.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f'captured {len(results)} route/viewport observations')
    print(f'screenshots {len(list(ROOT.glob("*.png")))}')
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
