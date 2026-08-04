#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request

routes = [
    '/',
    '/services/',
    '/services/refrigerator-repair/',
    '/service-areas/',
    '/service-areas/appliance-repair-corona-ca/',
    '/blog/',
    '/contact/',
    '/about-us/',
    '/search/?q=washer',
    '/es/',
    '/es/services/',
    '/es/services/refrigerator-repair/',
    '/es/service-areas/appliance-repair-corona-ca/',
    '/es/blog/',
    '/robots.txt',
    '/sitemap.xml',
    '/sitemap-images.xml',
    '/health/',
    '/no-such-page/',
]

base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:8057'
for path in routes:
    url = base + path
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            status = response.status
            data = response.read()
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        status = exc.code
        data = exc.read()
        final_url = exc.geturl()
    except Exception as exc:  # noqa: BLE001 - evidence script records any route failure
        print(f'{path:58} ERROR {type(exc).__name__}: {exc}')
        continue
    text = data.decode('utf-8', 'ignore')
    match = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
    title = re.sub(r'\s+', ' ', match.group(1)).strip() if match else ''
    print(f'{path:58} {status:<4} {len(data):7} {title} final={final_url}')
