#!/usr/bin/env python3
"""Start or reuse the local workbench; keep its process independent of this launcher."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
LOG = RUNTIME / "outputs" / "_service" / "workbench.log"


def ready(url: str) -> bool:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(url + "api/status", timeout=2) as response:
            status = json.load(response)
        return status.get("runtime") is True and len(status.get("skills", [])) == 113
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    host = os.getenv("SEAL_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("SEAL_PORT", "7862"))
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("SEAL_PORT must be between 1 and 65535.", file=sys.stderr)
        return 1
    health_host = "127.0.0.1" if host == "0.0.0.0" else host
    if ":" in health_host:
        health_host = f"[{health_host}]"
    url = f"http://{health_host}:{port}/"
    process = None
    if not ready(url):
        python = RUNTIME / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if not python.is_file():
            print("Runtime is missing. Run the installation script first.", file=sys.stderr)
            return 1
        LOG.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        command = [str(python), str(ROOT / "launch.py")]
        options = {}
        if os.name == "nt":
            options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        else:
            options["start_new_session"] = True
            xvfb = shutil.which("xvfb-run")
            if not env.get("DISPLAY") and xvfb:
                command = [xvfb, "-a", *command]
        try:
            with LOG.open("ab") as log:
                process = subprocess.Popen(
                    command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                    stdout=log, stderr=subprocess.STDOUT, **options,
                )
        except OSError as exc:
            print(f"Cannot start workbench: {exc}", file=sys.stderr)
            return 1
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if process.poll() is not None:
                print(f"Workbench exited. See startup log: {LOG}", file=sys.stderr)
                return 1
            if ready(url):
                break
            time.sleep(0.5)
        else:
            print(f"Startup is not ready. See startup log: {LOG}", file=sys.stderr)
            return 1
    print(f"Workbench ready: {url}")
    if args.no_browser:
        return 0
    if not webbrowser.open(url):
        print("Open this address in your browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
