#!/usr/bin/env python3
"""Fail CI on error diagnostics. Advisory warnings remain visible."""
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
files = report["fileinfos"]
errors = []
warnings = []
for file in files:
    for issue in file["diagnostics"]:
        if issue["severity"] == "Error":
            errors.append((file["path"], issue))
        elif issue["severity"] == "Warning":
            warnings.append((file["path"], issue))
for path, issue in errors + warnings:
    print(f'{issue["severity"]}: {path}:{issue["range"]["start"]["line"] + 1}: '
          f'{issue["code"]}: {issue["message"]}')
print(f"BSL LS: {len(files)} files, {len(errors)} errors, {len(warnings)} advisory warnings")
sys.exit(bool(errors))
