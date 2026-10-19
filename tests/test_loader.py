import tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.loader import discover

class LoaderTests(unittest.TestCase):
    def test_discovers_examples(self):
        root=Path(__file__).resolve().parents[1]
        items, errors=discover(root)
        self.assertGreaterEqual(len(items), 8)
        self.assertEqual(errors, [])
    def test_invalid_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'cron.d/daily').mkdir(parents=True)
            (root/'cron.d/daily/bad.skill.md').write_text('not frontmatter')
            items, errors=discover(root)
            self.assertEqual(len(items), 0); self.assertEqual(len(errors), 1)

if __name__ == '__main__': unittest.main()
