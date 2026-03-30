#!/usr/bin/env python3
import os
import sys
import subprocess

FILTER = os.path.expanduser("~/.scripts/homograph_filter.py")

def find_real_curl():
    """Find the real curl binary on macOS."""
    brew_paths = [
        "/opt/homebrew/bin/curl",
        "/usr/local/bin/curl"
    ]
    system_curl = "/usr/bin/curl"

    for path in brew_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    if os.path.isfile(system_curl) and os.access(system_curl, os.X_OK):
        return system_curl

    sys.stderr.write("❌ No curl binary found!\n")
    sys.exit(1)

REAL_CURL = find_real_curl()
args = sys.argv[1:]

# URL-only mode: validate a URL from stdin and exit 0 (clean) or 1 (homograph)
if args == ["--url-only"]:
    url = sys.stdin.read().strip()
    filter_proc = subprocess.run(
        ["python3", FILTER],
        input=url,
        text=True,
        capture_output=True
    )
    sys.exit(filter_proc.returncode)

# Check all arguments for homograph characters BEFORE executing curl
arg_check = subprocess.run(
    ["python3", FILTER],
    input="\n".join(args),
    text=True,
    capture_output=True
)
if arg_check.returncode != 0:
    sys.stderr.write("❌ Blocked: suspicious Unicode in curl arguments (possible homograph attack)\n")
    sys.exit(1)

# Arguments are clean — execute curl and filter the response
curl_proc = subprocess.Popen(
    [REAL_CURL] + args,
    stdout=subprocess.PIPE,
    bufsize=1,
    text=True
)

with subprocess.Popen(
    ["python3", FILTER],
    stdin=subprocess.PIPE,
    text=True
) as filter_proc:
    for line in curl_proc.stdout:
        filter_proc.stdin.write(line)
        filter_proc.stdin.flush()

curl_proc.stdout.close()
sys.exit(filter_proc.wait())
