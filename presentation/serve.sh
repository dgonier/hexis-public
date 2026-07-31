#!/usr/bin/env bash
# Serve the HEXIS deck over HTTP so Chrome's file:// XHR restrictions
# don't block <script type="text/babel" src="..."> from loading.
set -e
cd "$(dirname "$0")"
PORT="${PORT:-8000}"
URL="http://localhost:${PORT}/HEXIS%20Deck.html"
echo "→ Serving $(pwd) at ${URL}"
echo "→ Ctrl+C to stop."
# Best-effort browser open (mac/linux/wsl)
( sleep 1 && (xdg-open "$URL" 2>/dev/null \
  || open "$URL" 2>/dev/null \
  || powershell.exe Start "$URL" 2>/dev/null \
  || true) ) &
exec python3 -m http.server "$PORT"
