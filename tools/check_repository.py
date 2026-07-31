#!/usr/bin/env python3
"""Check local Markdown links and publication-sensitive text."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_PATH_RE = re.compile(r"/Users/[^/\s]+/")
SECRET_RE = re.compile(r"sk-[A-Za-z0-9_-]{20,}")


def main():
    failures = []

    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")

        for target in LINK_RE.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(
                ("http://", "https://", "mailto:")
            ):
                continue
            resolved = (markdown.parent / unquote(target)).resolve()
            if not resolved.exists():
                failures.append(
                    f"broken link in {markdown.relative_to(ROOT)}: {target}"
                )

        if ABSOLUTE_PATH_RE.search(text):
            failures.append(
                f"local absolute path in {markdown.relative_to(ROOT)}"
            )

        if SECRET_RE.search(text):
            failures.append(
                f"possible API secret in {markdown.relative_to(ROOT)}"
            )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        sys.exit(1)

    print("Repository publication checks passed.")


if __name__ == "__main__":
    main()
