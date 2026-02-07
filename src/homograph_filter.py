#!/usr/bin/env python3
import sys
import unicodedata

def suspicious_char(c):
    if ord(c) <= 127:
        return False
    try:
        name = unicodedata.name(c)
        if not name.startswith("LATIN"):
            return True
    except ValueError:
        return True
    return False

def suspicious_line(line):
    normalized = unicodedata.normalize("NFKC", line)
    if normalized != line:
        return True
    for c in normalized:
        if suspicious_char(c):
            return True
    return False

for line in sys.stdin:
    if suspicious_line(line):
        print("❌ Blocked: suspicious Unicode (possible homograph attack)", file=sys.stderr)
        sys.exit(1)
    # Print safe content only
    print(line, end="")
