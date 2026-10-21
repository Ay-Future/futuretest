[![英语](https://img.shields.io/badge/English-lightgrey)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-blue)](README.zh-CN.md)

# 业务上下文

基于 Deep Agents 的业务上下文公共输入能力。输入需求材料，整理业务规则、系统映射和场景，经确认及确定性校验后发布版本化测试上下文包。

当前为项目框架阶段：已提供 Python 包结构、命令行入口、运行目录初始化和基础测试。材料导入、Pydantic 模型、Deep Agents 分析、SQLite 事实存储、运行恢复、确认及发布将在后续阶段实现。

实施依据：[实施计划](DeepAgents业务上下文公共输入能力实施计划.md)。当前仓库根目录对应计划中的 `business-context/`，无需再创建一层同名目录。

## 快速开始

需要 Python 3.11 或以上及 uv。在仓库根目录执行：

```powershell
uv sync --locked
uv run business-context --help
uv run business-context --version
uv run business-context init
uv run python -m unittest discover -s tests -v
```

也可使用标准 Python 工具：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\business-context.exe init
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

框架目前仅使用 Python 标准库，无模型调用和密钥要求。`uv.lock` 记录当前框架的依赖状态。Deep Agents、Pydantic、持久化检查点保存组件及模型服务依赖应在 D2–D4 接入并验证后加入、更新锁文件；当前锁文件不代表这些技术已完成验证。

## 项目结构

```text
schemas/                   六类核心对象的 JSON 结构规范（待定义）
src/
  ingest/                  材料导入、快照、哈希及定位
  agent/                   主智能体配置、提示词和受控工具
  facts/                   事实查询、版本管理及确认记录
  workflow/                命令行入口、运行配置；后续状态机、恢复与发布
  validation/              发布前的确定性约束
  adapters/                用例生成与接口自动化适配
skills/                    四项项目方法的预留目录
examples/                  脱敏样例
evals/                     开发数据与评测入口
tests/                     框架及关键约束测试
docs/                      接入契约、操作说明与验收记录
```

目录直接采用计划中的六个 Python 包名；通过安装项目加载 `src/` 下的包，不需要手动修改 `PYTHONPATH`。

## 运行数据

`business-context init` 默认在当前工作目录的 `.data/` 下创建 `sources/`、`drafts/`、`packages/` 和 `runs/`。命令可重复执行，不覆盖已有文件。它只初始化目录；事实数据库和智能体检查点数据库由后续对应模块创建。

```powershell
uv run business-context init --data-dir D:\business-context-data
# 或使用环境变量；显式 --data-dir 的优先级更高
$env:BUSINESS_CONTEXT_DATA_DIR = 'D:\business-context-data'
uv run business-context init
```

`.env.example` 仅用于说明环境变量，不会自动加载。`.data/`、`data/` 和本地数据库已被 Git 忽略；自定义运行目录建议放在仓库外。真实材料、账号凭据和留出评测答案应存放在独立受控目录。

后续实现边界见 [架构说明](docs/architecture.md)，阶段清单见 [开发路线](docs/development.md)。
