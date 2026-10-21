"""项目命令行入口。"""

import argparse
from importlib.metadata import version
from typing import Sequence

from workflow.config import RuntimePaths


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="business-context",
        description="业务上下文公共输入能力：项目框架及运行目录管理。",
    )
    parser.add_argument(
        "--version", action="version", version=version("business-context")
    )
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init", help="创建运行数据目录，不覆盖已有内容")
    initialize.add_argument("--data-dir", help="运行数据目录，默认读取环境变量或使用 .data")
    args = parser.parse_args(argv)

    if args.command == "init":
        try:
            paths = RuntimePaths.from_environment(args.data_dir)
            paths.initialize()
        except (OSError, ValueError) as error:
            parser.exit(status=1, message=f"初始化失败：{error}\n")
        print(f"运行目录已就绪：{paths.root}")
        print("sources/  drafts/  packages/  runs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
