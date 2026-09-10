#!/usr/bin/env python3
"""Derive the claude.ai Artifact version of the tracker from the standalone page.

The Artifact host supplies its own <!doctype>, <html>, <head> and <body>, so the
published file carries only the page content: title, font/library links, styles
and markup. Everything else is byte-identical to index.html, which stays the
canonical source — edit that file, then re-run this script.

    python3 build_artifact.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "index.html"
OUT = HERE / "artifact.html"

html = SRC.read_text()

head = html[html.index("<title>"):html.index("</head>")]
head = re.sub(r'^\s*<meta[^>]*>\s*$\n?', '', head, flags=re.MULTILINE)

body = html[html.index("<body>") + len("<body>"):html.rindex("</body>")]

OUT.write_text(head.rstrip() + "\n" + body.rstrip() + "\n")

written = OUT.read_text().lower()
for tag in ("<!doctype", "html", "head", "body"):
    if re.search(r"<%s(?=[\s>])" % re.escape(tag.lstrip("<")), written):
        sys.exit("error: <%s> survived into %s" % (tag, OUT.name))

print("wrote %s (%d bytes)" % (OUT.name, OUT.stat().st_size))
