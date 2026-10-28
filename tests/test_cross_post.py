"""Tests for skills/launch-cross-post/scripts/prepare-article.py."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "skills" / "launch-cross-post" / "scripts" / "prepare-article.py"
CANONICAL = "https://example.dev/en/blog/tool/"

POST = """---
title: "Tool: a title with a colon"
description: "Why I built it."
pubDate: 2026-10-26
cover: ./cover.webp
tags: ["Launch", "macOS"]
---

Intro paragraph.

![Settings](./settings.webp)

```bash
echo "![not an image](./code.png)"
```
"""


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class PrepareArticle(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.post = pathlib.Path(self.dir.name) / "en.md"
        self.post.write_text(POST)
        self.out = pathlib.Path(self.dir.name) / "out"

    def tearDown(self):
        self.dir.cleanup()

    def prepare(self, *extra):
        return run(str(self.post), "--canonical", CANONICAL, "--out", str(self.out),
                   "--asset", "./settings.webp=https://cdn.example/settings.webp", *extra)

    def test_body_drops_front_matter_and_maps_images(self):
        r = self.prepare()
        self.assertEqual(r.returncode, 0, r.stderr)
        body = (self.out / "body.md").read_text()
        self.assertTrue(body.startswith("Intro paragraph."))
        self.assertIn("![Settings](https://cdn.example/settings.webp)", body)

    def test_code_blocks_are_left_alone(self):
        self.prepare()
        self.assertIn('echo "![not an image](./code.png)"', (self.out / "body.md").read_text())

    def test_footer_links_the_canonical_post(self):
        self.prepare()
        body = (self.out / "body.md").read_text()
        self.assertTrue(body.rstrip().endswith(f"*Originally published on [my blog]({CANONICAL}).*"))

    def test_meta_carries_fields_for_each_platform(self):
        self.prepare()
        meta = json.loads((self.out / "meta.json").read_text())
        self.assertEqual(meta["title"], "Tool: a title with a colon")
        self.assertEqual(meta["description"], "Why I built it.")
        self.assertEqual(meta["canonical_url"], CANONICAL)
        self.assertEqual(meta["cover"], "./cover.webp")

    def test_unmapped_relative_image_fails_without_output(self):
        r = run(str(self.post), "--canonical", CANONICAL, "--out", str(self.out))
        self.assertEqual(r.returncode, 2)
        self.assertIn("./settings.webp", r.stderr)
        self.assertFalse(self.out.exists())

    def test_canonical_must_be_https(self):
        r = run(str(self.post), "--canonical", "http://example.dev/x", "--out", str(self.out),
                "--asset", "./settings.webp=https://cdn.example/settings.webp")
        self.assertEqual(r.returncode, 2)

    def test_footer_text_can_be_changed(self):
        self.prepare("--footer", "Publicado originalmente en [mi blog]({url}).")
        self.assertIn(f"*Publicado originalmente en [mi blog]({CANONICAL}).*", (self.out / "body.md").read_text())


if __name__ == "__main__":
    unittest.main()
