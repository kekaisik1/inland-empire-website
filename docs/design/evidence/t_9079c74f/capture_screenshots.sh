#!/usr/bin/env bash
set -euo pipefail
BASE=${1:-http://127.0.0.1:8057}
OUT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME=${CHROME_BIN:-google-chrome}
PROFILE_ROOT="$(mktemp -d)"
cleanup() { rm -rf "$PROFILE_ROOT"; }
trap cleanup EXIT
capture() {
  local vp="$1" w="$2" h="$3" name="$4" path="$5"
  local out="$OUT_DIR/${vp}__${name}.png"
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size="${w},${h}" --user-data-dir="$PROFILE_ROOT/$vp-$name" --screenshot="$out" "$BASE$path" >/dev/null 2>&1
  python -c "from pathlib import Path; p=Path('$out'); print(f'{p.name} {p.stat().st_size} bytes')"
}
capture desktop-1440x900 1440 900 home-en /
capture mobile-390x844 390 844 home-en /
capture tablet-768x1024 768 1024 home-en /
capture desktop-1440x900 1440 900 services-en /services/
capture desktop-1440x900 1440 900 service-refrigerator-en /services/refrigerator-repair/
capture mobile-390x844 390 844 service-refrigerator-en /services/refrigerator-repair/
capture desktop-1440x900 1440 900 areas-en /service-areas/
capture desktop-1440x900 1440 900 city-corona-en /service-areas/appliance-repair-corona-ca/
capture mobile-390x844 390 844 city-corona-en /service-areas/appliance-repair-corona-ca/
capture desktop-1440x900 1440 900 blog-en /blog/
capture desktop-1440x900 1440 900 contact-en /contact/
capture desktop-1440x900 1440 900 search-en '/search/?q=washer'
capture desktop-1440x900 1440 900 home-es /es/
capture mobile-390x844 390 844 home-es /es/
capture mobile-390x844 390 844 service-refrigerator-es /es/services/refrigerator-repair/
capture desktop-1440x900 1440 900 city-corona-es /es/service-areas/appliance-repair-corona-ca/
capture desktop-1440x900 1440 900 blog-es /es/blog/
