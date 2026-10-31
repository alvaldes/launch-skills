"""Tests for the launch-lists scripts. Run: python3 -m unittest discover -s tests"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "launch-lists" / "scripts"

README = """# List

## Utilities

### Productivity

* [Hyperkey](https://hyperkey.app/) - Turn Caps Lock into a Hyper key.
* [iCMD](https://icmd.app) - Global fuzzy menu search.
* [Karabiner-Elements](https://karabiner-elements.pqrs.org/) - Remap keys.

### Window Management

* [Rectangle](https://rectangleapp.com/) - Move and resize windows.
"""

APPS = """{
    "applications": [
        {
            "title": "KeyEcho",
            "short_description": "Keyboard sounds.",
            "repo_url": "https://github.com/ZacharyL2/KeyEcho"
        }
    ]
}
"""

ENTRY = {
    "title": "JUMP",
    "short_description": "Click anything from the keyboard.",
    "categories": ["keyboard"],
    "repo_url": "https://github.com/alvaldes/jump",
    "icon_url": "",
    "screenshots": [],
    "official_site": "https://alvaldes.github.io/jump/",
    "languages": ["swift"],
}

LINE = "* [JUMP](https://alvaldes.github.io/jump/) - Click anything from the keyboard."


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True)


class InsertListLine(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = pathlib.Path(self.dir.name) / "README.md"
        self.file.write_text(README)

    def tearDown(self):
        self.dir.cleanup()

    def test_inserts_alphabetically_ignoring_case(self):
        r = run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", LINE)
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = self.file.read_text().splitlines()
        i = lines.index(LINE)
        self.assertTrue(lines[i - 1].startswith("* [iCMD]"))
        self.assertTrue(lines[i + 1].startswith("* [Karabiner-Elements]"))

    def test_only_one_line_changes(self):
        run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", LINE)
        self.assertEqual(len(self.file.read_text().splitlines()), len(README.splitlines()) + 1)

    def test_appends_after_last_item_when_name_sorts_last(self):
        line = "* [Zed](https://zed.dev) - Editor."
        run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", line)
        lines = self.file.read_text().splitlines()
        i = lines.index(line)
        self.assertTrue(lines[i - 1].startswith("* [Karabiner-Elements]"))
        self.assertEqual(lines[i + 1], "")

    def test_accented_names_sort_by_their_base_letter(self):
        self.file.write_text(
            "### Menu Bar Tools\n\n"
            "* [cctop](https://cctop.app) - Sessions.\n"
            "* [Çentik](https://example.com/centik) - Notch.\n"
            "* [ChargeMonitor](https://example.com/charge) - Battery.\n"
            "* [NetFluss](https://example.com/netfluss) - Speeds.\n"
            "* [Notchly](https://example.com/notchly) - Notch.\n"
        )
        line = "* [Netty](https://alvaldes.github.io/netty/) - Internet status."
        r = run("insert-list-line.py", str(self.file), "--section", "### Menu Bar Tools", "--line", line)
        self.assertEqual(r.returncode, 0, r.stderr)
        names = [l.split("]")[0][3:] for l in self.file.read_text().splitlines() if l.startswith("* [")]
        self.assertEqual(names, ["cctop", "Çentik", "ChargeMonitor", "NetFluss", "Netty", "Notchly"])

    def test_refuses_duplicate_name(self):
        run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", LINE)
        r = run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", LINE)
        self.assertEqual(r.returncode, 1)
        self.assertIn("already", r.stderr)
        self.assertEqual(self.file.read_text().count("[JUMP]"), 1)

    def test_unknown_section_fails_without_writing(self):
        r = run("insert-list-line.py", str(self.file), "--section", "### Nope", "--line", LINE)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.file.read_text(), README)

    def test_dash_bullets_are_supported(self):
        self.file.write_text(README.replace("* [", "- ["))
        line = LINE.replace("* [", "- [")
        r = run("insert-list-line.py", str(self.file), "--section", "### Productivity", "--line", line)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(line, self.file.read_text())


class AddJsonEntry(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.apps = pathlib.Path(self.dir.name) / "applications.json"
        self.apps.write_text(APPS)
        self.entry = pathlib.Path(self.dir.name) / "entry.json"
        self.entry.write_text(json.dumps(ENTRY))

    def tearDown(self):
        self.dir.cleanup()

    def test_appends_entry_last_and_stays_valid(self):
        r = run("add-json-entry.py", str(self.apps), str(self.entry))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(self.apps.read_text())
        self.assertEqual([a["title"] for a in data["applications"]], ["KeyEcho", "JUMP"])

    def test_keeps_existing_text_and_indentation(self):
        run("add-json-entry.py", str(self.apps), str(self.entry))
        text = self.apps.read_text()
        self.assertTrue(text.startswith(APPS.split("        }\n    ]")[0]))
        self.assertIn('\n        {\n            "title": "JUMP",', text)
        self.assertTrue(text.endswith("    ]\n}\n"))

    def test_refuses_duplicate_repo(self):
        run("add-json-entry.py", str(self.apps), str(self.entry))
        r = run("add-json-entry.py", str(self.apps), str(self.entry))
        self.assertEqual(r.returncode, 1)
        self.assertIn("already", r.stderr)

    def test_requires_description_ending_with_period(self):
        bad = dict(ENTRY, short_description="No period")
        self.entry.write_text(json.dumps(bad))
        r = run("add-json-entry.py", str(self.apps), str(self.entry))
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.apps.read_text(), APPS)


if __name__ == "__main__":
    unittest.main()
