"""检查初始化的配置优先级、幂等性和错误出口。"""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from workflow.cli import main
from workflow.config import RuntimePaths


class BootstrapTests(unittest.TestCase):
    def test_explicit_path_overrides_environment(self) -> None:
        with TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"BUSINESS_CONTEXT_DATA_DIR": "unused"}):
                paths = RuntimePaths.from_environment(directory)
            self.assertEqual(paths.root, Path(directory).resolve())

    def test_environment_selects_runtime_directory(self) -> None:
        with TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"BUSINESS_CONTEXT_DATA_DIR": directory}):
                self.assertEqual(
                    RuntimePaths.from_environment().root, Path(directory).resolve()
                )

    def test_init_is_repeatable_and_preserves_existing_data(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory) / "runtime"
            with redirect_stdout(StringIO()):
                self.assertEqual(main(["init", "--data-dir", str(root)]), 0)
                evidence = root / "sources" / "existing.txt"
                evidence.write_text("existing evidence", encoding="utf-8")
                self.assertEqual(main(["init", "--data-dir", str(root)]), 0)
            for name in ("sources", "drafts", "packages", "runs"):
                self.assertTrue((root / name).is_dir())
            self.assertEqual(evidence.read_text(encoding="utf-8"), "existing evidence")
            self.assertFalse((root / "facts.sqlite3").exists())
            self.assertFalse((root / "runs" / "checkpoints.sqlite3").exists())

    def test_path_conflict_returns_failure(self) -> None:
        with TemporaryDirectory() as directory:
            conflict = Path(directory) / "sources"
            conflict.write_text("keep me", encoding="utf-8")
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as raised:
                main(["init", "--data-dir", directory])
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(conflict.read_text(encoding="utf-8"), "keep me")


if __name__ == "__main__":
    unittest.main()
