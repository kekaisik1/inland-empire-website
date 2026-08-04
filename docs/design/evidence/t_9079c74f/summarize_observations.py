#!/usr/bin/env python3
from __future__ import annotations

import collections
import json
from pathlib import Path

data = json.loads(Path(__file__).with_name('browser-observations.json').read_text())
print('entries', len(data))
err_counter: collections.Counter[str] = collections.Counter()
for item in data:
    for event in item['errors']:
        params = event.get('params', {})
        key = event['method'] + ':' + str(params.get('errorText') or params.get('entry', {}).get('level') or params.get('type') or '')
        err_counter[key] += 1
print('error_summary', dict(err_counter))
print('overflow', [(x['route'], x['viewport'], x['observations']['scrollWidth'], x['observations']['innerWidth']) for x in data if x['observations'].get('horizontalOverflow')])
print('lowl_routes', sorted(set(x['route'] for x in data if x['observations'].get('bodyMentionsLOWL'))))
print('missing_images_total', sum(len(x['observations'].get('missingImages') or []) for x in data))
print('mobile_menu', [(x['route'], x['viewport'], x.get('mobile_menu_after_click')) for x in data if 'mobile_menu_after_click' in x])
print('small_target_entries', sum(1 for x in data if x['observations'].get('smallTargets')))
print('unnamed_entries', sum(1 for x in data if x['observations'].get('unnamedControls')))
for item in data[:3]:
    print('sample', item['route'], item['viewport'], item['observations']['title'], item['observations']['h1'], 'small=', item['observations'].get('smallTargets')[:3], 'unnamed=', item['observations'].get('unnamedControls')[:2], 'booking=', item['observations'].get('bookingLinks'))
