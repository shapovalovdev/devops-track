#!/usr/bin/env python3
"""Does Russian search actually return results on the built site?

This exists because the failure it catches is silent. The site builds, the
search box appears, the index file is full of Cyrillic — and typing a Russian
word returns nothing. Nobody notices, because nobody searches a site they
wrote themselves.

    ./site/build.sh && python3 site/test_search.py

Requires playwright (`pip install playwright && playwright install chromium`).
Skips itself if playwright is missing, so it never blocks a build.

Two traps are baked into this file; both cost an hour the first time.

1.  Material runs the search on `keyup`. Playwright inserts non-ASCII text
    without emitting key events, so a Cyrillic query typed by a test sits in
    the box and never runs — which looks exactly like a broken index. Hence
    the `End` keypress after typing.

2.  Every query below is in a different grammatical form than the text on the
    page ("контейнеры" where pages say "контейнер"). Search matches by prefix,
    not by stem — see the long comment in mkdocs.yml — so these queries pass
    only because the prefix survives, and they will fail loudly if someone
    turns the stemmer on to "improve" things.
"""

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT = 8137

# Two layouts, on purpose. In this repo the file lives in site/ and the build
# lands in site/_build. Published, it sits at the root of the public repo next
# to _build, and runs there as a CI gate — same file, so the check that guards
# the laptop is literally the one that guards the deploy.
BUILD = next(
    (p for p in (HERE.parent / "site" / "_build", HERE / "_build") if p.is_dir()),
    HERE / "_build",
)

# One edition per entry: URL path under the built site, and the queries that
# must return something there. Each edition carries its own search index built
# by its own config, so each has to be checked on its own.
EDITIONS = [
    ("ru", "/", [
        "рукопожатие",   # tasks / theory / questions
        "контейнеры",    # plural where the text is singular
        "сети",          # oblique case
        "отсыпной",      # rare word, only in the slot table
        "runner",        # latin inside a Russian page
        "handshake",
    ]),
    ("en", "/en/", [
        "handshake",
        "containers",    # plural where the text is singular
        "networking",
        "runner",
        "pipeline",
        "recovery",      # from the slot table
    ]),
]


def check_edition(page, base, queries):
    page.goto(base, wait_until="networkidle")
    box = page.locator("input.md-search__input")
    box.click()
    page.wait_for_timeout(1500)      # let the worker build the index

    results = {}
    for query in queries:
        box.fill("")
        box.type(query, delay=20)
        page.keyboard.press("End")   # see trap 1 above
        page.wait_for_timeout(800)
        results[query] = page.locator(".md-search-result__item").count()
    return results


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP: playwright not installed")
        return 0

    if not (BUILD / "index.html").is_file():
        print(f"FAIL: {BUILD} not built — run ./site/build.sh first")
        return 1

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--directory", str(BUILD)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.5)
        results = {}
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1200, "height": 900})
            for code, path, queries in EDITIONS:
                if not (BUILD / path.strip("/") / "index.html").is_file() \
                        and path != "/":
                    print(f"FAIL: the {code} edition was not built at {path}")
                    return 1
                for query, n in check_edition(
                        page, f"http://localhost:{PORT}{path}", queries).items():
                    results[f"[{code}] {query}"] = n
            browser.close()
    finally:
        server.terminate()

    failed = [q for q, n in results.items() if n == 0]
    for query, n in results.items():
        print(f"{'ok  ' if n else 'FAIL'} {query}: {n} hit(s)")

    if failed:
        print(f"\nFAIL: no results for {failed}")
        print("Check `plugins.search.pipeline` in the relevant mkdocs config "
              "before anything else — mkdocs.yml for [ru], mkdocs.en.yml for [en].")
        return 1

    print(f"\nOK — search returns results in {len(EDITIONS)} editions, both scripts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
