"""运行数据位置；业务事实与 Agent 运行状态使用独立存储。"""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    root: Path

    @classmethod
    def from_environment(cls, data_dir: str | Path | None = None) -> "RuntimePaths":
        configured = (
            data_dir
            if data_dir is not None
            else os.environ.get("BUSINESS_CONTEXT_DATA_DIR") or ".data"
        )
        return cls(root=Path(configured).expanduser().resolve())

    @property
    def sources(self) -> Path:
        return self.root / "sources"

    @property
    def drafts(self) -> Path:
        return self.root / "drafts"

    @property
    def packages(self) -> Path:
        return self.root / "packages"

    @property
    def runs(self) -> Path:
        return self.root / "runs"

    @property
    def facts_database(self) -> Path:
        return self.root / "facts.sqlite3"

    @property
    def checkpoints_database(self) -> Path:
        return self.runs / "checkpoints.sqlite3"

    def initialize(self) -> None:
        """仅创建目录；不生成或覆盖业务资料及数据库。"""
        for directory in (self.sources, self.drafts, self.packages, self.runs):
            directory.mkdir(parents=True, exist_ok=True)
