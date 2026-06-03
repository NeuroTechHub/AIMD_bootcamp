"""Serve the bootcamp HTML modules from the repo root on http://127.0.0.1:8889.

Why: Jupyter's /files/ endpoint sandboxes responses (blocks fetch + getUserMedia),
and file:// has the same restrictions. A plain HTTP origin on 127.0.0.1 is a
secure context, so M1's webcam + bus-detection JSON and M5's e2e weights all
load correctly. Run with:

    uv run html_modules.py
"""
from __future__ import annotations

import http.server
import socketserver
import sys
from functools import partial
from pathlib import Path

PORT = 8889
ROOT = Path(__file__).resolve().parent


def main() -> int:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    try:
        with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), handler) as httpd:
            httpd.allow_reuse_address = True
            print(f"Serving {ROOT}")
            print(f"  bootcamp plan : http://127.0.0.1:{PORT}/bootcamp-plan.html")
            print(f"  modules index : http://127.0.0.1:{PORT}/modules/")
            print("Ctrl-C to stop.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
        return 0
    except OSError as exc:
        print(f"could not bind 127.0.0.1:{PORT} — {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
