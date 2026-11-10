#!/usr/bin/env python3
"""Собирает dist/ из шаблона index.html, подставляя секреты из окружения."""
import os
import re
import shutil
import sys
from pathlib import Path

PLACEHOLDERS = [
    "NAME_FULL",
    "NAME_FULL_GEN",
    "NAME_FIRST",
    "NAME_FIRST_GEN",
    "TELEGRAM",
    "CONTACT_EMAIL",
]

missing = [n for n in PLACEHOLDERS if not os.environ.get(n)]
if missing:
    sys.exit(f"Не заданы переменные: {', '.join(missing)}")

html = Path("index.html").read_text(encoding="utf-8")
for name in PLACEHOLDERS:
    html = html.replace("{{" + name + "}}", os.environ[name])

leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
if leftover:
    sys.exit(f"Незаменённые плейсхолдеры: {', '.join(leftover)}")

dist = Path("dist")
if dist.exists():
    shutil.rmtree(dist)
dist.mkdir()
(dist / "index.html").write_text(html, encoding="utf-8")
shutil.copytree("static", dist / "static")
shutil.copy2("robots.txt", dist / "robots.txt")
print("Готово: dist/ собран.")
