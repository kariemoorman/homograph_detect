#!/usr/bin/env python3
import os
import sys
import subprocess

FILTER = os.path.expanduser("~/homograph_filter.py")

def find_real_curl():
    system_curl = "/usr/bin/curl"
    brew_paths = [
        "/opt/homebrew/bin/curl",
        "/usr/local/bin/curl"
    ]

    for path in brew_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    if os.path.isfile(system_curl) and os.access(system_curl, os.X_OK):
        return system_curl

    sys.stderr.write("❌ No curl binary found!\n")
    sys.exit(1)

REAL_CURL = find_real_curl()

args = sys.argv[1:]

if sys.stdout.isatty():
    os.execv(REAL_CURL, ["curl"] + args)

curl_proc = subprocess.Popen(
    [REAL_CURL] + args,
    stdout=subprocess.PIPE
)

filter_proc = subprocess.Popen(
    ["python3", FILTER],
    stdin=curl_proc.stdout
)

curl_proc.stdout.close()
sys.exit(filter_proc.wait())
