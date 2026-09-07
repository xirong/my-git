#!/usr/bin/env python3
"""Regression coverage for the two local-link checker entry paths."""
from __future__ import annotations

import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_module(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CHECK_DOCS = load_module("check-docs.py", "check_docs_for_test")
CHECK_LINKS = load_module("check-links.py", "check_links_for_test")


class LocalLinkCheckerRegressionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(
            prefix=".link-check-fixture-", dir=SCRIPTS_DIR
        )
        self.fixture_root = Path(self.temp_dir.name)
        self.document = self.fixture_root / "guide.md"
        self.document.write_text("# fixture\n", encoding="utf-8")
        (self.fixture_root / "existing.html").write_text("ok\n", encoding="utf-8")
        (self.fixture_root / "空 白.html").write_text("ok\n", encoding="utf-8")
        (self.fixture_root / "hash#name.html").write_text("ok\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def assert_local_result(self, raw: str, *, broken: bool = False) -> None:
        self.document.write_text(f"[fixture]({raw})\n", encoding="utf-8")
        docs_errors = CHECK_DOCS.check_local_links([self.document])
        occurrence = CHECK_LINKS.LinkOccurrence(self.document, 1, raw)
        links_errors = CHECK_LINKS.check_local_links([occurrence])

        if broken:
            self.assertEqual(len(docs_errors), 1, docs_errors)
            self.assertEqual(len(links_errors), 1, links_errors)
            return

        self.assertEqual(docs_errors, [])
        self.assertEqual(links_errors, [])

    def test_existing_path_ignores_query_and_fragment(self) -> None:
        self.assert_local_result("existing.html?lang=en#fragment")
        self.assert_local_result("<existing.html?lang=en#fragment>")

    def test_whitespace_and_unicode_path(self) -> None:
        self.assert_local_result("  <空 白.html?lang=zh#标题>  ")

    def test_encoded_hash_stays_in_filename(self) -> None:
        self.assert_local_result("hash%23name.html?lang=en#fragment")

    def test_missing_path_with_query_fails(self) -> None:
        self.assert_local_result("missing.html?lang=en", broken=True)

    def test_fragment_and_query_only_targets_do_not_require_a_file(self) -> None:
        self.assert_local_result("#section")
        self.assert_local_result("?lang=en")

    def test_pages_url_with_query_and_fragment_maps_to_source(self) -> None:
        url = "https://xirong.github.io/my-git/README.md?lang=en#course"
        self.assertEqual(CHECK_LINKS.repo_pages_target(url), (REPO_ROOT / "README.md").resolve())
        occurrence = CHECK_LINKS.LinkOccurrence(self.document, 1, url)
        self.assertEqual(CHECK_LINKS.external_urls([occurrence]), {})

    def test_missing_pages_url_fails_even_without_external_checks(self) -> None:
        url = (
            "https://xirong.github.io/my-git/interactive/"
            "definitely-missing.html?lang=en#x"
        )
        self.document.write_text(f"[missing]({url})\n", encoding="utf-8")
        occurrence = CHECK_LINKS.LinkOccurrence(self.document, 1, url)

        self.assertEqual(len(CHECK_DOCS.check_local_links([self.document])), 1)
        self.assertEqual(len(CHECK_LINKS.check_local_links([occurrence])), 1)
        self.assertEqual(CHECK_LINKS.external_urls([occurrence]), {})

        with (
            mock.patch.object(CHECK_LINKS, "markdown_files", return_value=[self.document]),
            mock.patch.object(sys, "argv", ["check-links.py", "--no-external"]),
            mock.patch("sys.stdout", new_callable=io.StringIO) as output,
        ):
            self.assertEqual(CHECK_LINKS.main(), 1)
        self.assertIn("broken local link", output.getvalue())

    def test_missing_pages_url_makes_no_external_cli_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="my-git-link-cli-") as temp_dir:
            temp_root = Path(temp_dir)
            temp_scripts = temp_root / "scripts"
            temp_scripts.mkdir()
            for filename in ("check-links.py", "link_targets.py"):
                shutil.copy2(SCRIPTS_DIR / filename, temp_scripts / filename)
            (temp_root / "README.md").write_text(
                "[missing](https://xirong.github.io/my-git/interactive/"
                "definitely-missing.html?lang=en#x)\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(temp_scripts / "check-links.py"), "--no-external"],
                cwd=temp_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("broken local link", result.stdout)
            self.assertFalse((temp_scripts / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
