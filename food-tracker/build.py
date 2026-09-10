#!/usr/bin/env python3
"""Build the two published copies of the tracker from index.html.

index.html is the canonical source — edit it, then re-run this script.

  docs/food-tracker/index.html   verbatim copy, served by GitHub Pages
  food-tracker/artifact.html     the claude.ai Artifact body

The Artifact host supplies its own <!doctype>, <html>, <head> and <body>, so that
copy carries only the page content: title, font/library links, styles and markup.

    python3 food-tracker/build.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "index.html"
OUT = HERE / "artifact.html"
PAGES = HERE.parent / "docs" / "food-tracker" / "index.html"

html = SRC.read_text()

PAGES.parent.mkdir(parents=True, exist_ok=True)
PAGES.write_text(html)

head = html[html.index("<title>"):html.index("</head>")]
head = re.sub(r'^\s*<meta[^>]*>\s*$\n?', '', head, flags=re.MULTILINE)

body = html[html.index("<body>") + len("<body>"):html.rindex("</body>")]

OUT.write_text(head.rstrip() + "\n" + body.rstrip() + "\n")

written = OUT.read_text().lower()
for tag in ("<!doctype", "html", "head", "body"):
    if re.search(r"<%s(?=[\s>])" % re.escape(tag.lstrip("<")), written):
        sys.exit("error: <%s> survived into %s" % (tag, OUT.name))

print("wrote %s (%d bytes)" % (PAGES.relative_to(HERE.parent), PAGES.stat().st_size))
print("wrote %s (%d bytes)" % (OUT.relative_to(HERE.parent), OUT.stat().st_size))
