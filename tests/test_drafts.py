"""Tests for skills/launch-community-drafts/scripts/check-draft.py."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "skills" / "launch-community-drafts" / "scripts" / "check-draft.py"


def check(text, channel):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(text)
    try:
        return subprocess.run([sys.executable, str(SCRIPT), f.name, "--channel", channel], capture_output=True, text=True)
    finally:
        pathlib.Path(f.name).unlink()


class CheckDraft(unittest.TestCase):
    def test_clean_draft_passes(self):
        r = check("I built JUMP. It is free.", "threads")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_em_dash_is_flagged(self):
        r = check("I built it — for me.", "reddit")
        self.assertEqual(r.returncode, 1)
        self.assertIn("em dash", r.stdout)

    def test_threads_limit_is_500_characters(self):
        self.assertEqual(check("a" * 500, "threads").returncode, 0)
        r = check("a" * 501, "threads")
        self.assertEqual(r.returncode, 1)
        self.assertIn("501/500", r.stdout)

    def test_x_checks_each_post_of_a_thread(self):
        thread = "short post\n\n---\n\n" + "b" * 281
        r = check(thread, "x")
        self.assertEqual(r.returncode, 1)
        self.assertIn("post 2", r.stdout)

    def test_show_hn_title_must_start_with_show_hn(self):
        r = check("title: JUMP for macOS\n\nBody.", "show-hn")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Show HN:", r.stdout)

    def test_reddit_pcp_needs_the_three_parts(self):
        r = check("[OS] Tool\n\nProblem: x\n\nPricing: Free", "reddit-pcp")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Comparison:", r.stdout)

    def test_reddit_pcp_rejects_direct_download_links(self):
        text = "Problem: x\nComparison: y\nPricing: Free https://x.com/a/releases/download/App.dmg"
        r = check(text, "reddit-pcp")
        self.assertEqual(r.returncode, 1)
        self.assertIn(".dmg", r.stdout)

    def test_unknown_channel_exits_2(self):
        self.assertEqual(check("x", "myspace").returncode, 2)


if __name__ == "__main__":
    unittest.main()
