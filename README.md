[![English](https://img.shields.io/badge/English-blue)](README.md) [![Chinese](https://img.shields.io/badge/简体中文-lightgrey)](README.zh-CN.md)

# Business Context

A shared business context capability built on Deep Agents. It takes requirement materials, organizes business rules, system mappings, and scenarios, then publishes versioned test context packages after confirmation and deterministic validation.

The project is currently a scaffold with a Python package structure, a command-line entry point, runtime directory initialization, and basic tests. Material ingestion, Pydantic models, Deep Agents analysis, SQLite fact storage, run recovery, confirmation, and publishing will be implemented in later stages.

The project follows the [implementation plan](DeepAgents业务上下文公共输入能力实施计划.md). The repository root corresponds to `business-context/` in the plan; no additional directory with that name is needed.

## Quick start

Requires Python 3.11 or later and uv. Run these commands from the repository root:

```powershell
uv sync --locked
uv run business-context --help
uv run business-context --version
uv run business-context init
uv run python -m unittest discover -s tests -v
```

Alternatively, use the standard Python tools:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\business-context.exe init
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The scaffold currently uses only the Python standard library and requires no model calls or API keys. `uv.lock` records its current dependency state. Dependencies for Deep Agents, Pydantic, a persistent checkpointer, and the model service should be added and the lockfile updated after integration and verification during D2–D4. The current lockfile does not indicate that these technologies have been verified.

## Project structure

```text
schemas/                   JSON Schemas for six core objects (to be defined)
src/
  ingest/                  Material ingestion, snapshots, hashing, and source locations
  agent/                   Main agent configuration, prompts, and controlled tools
  facts/                   Fact queries, version management, and confirmation records
  workflow/                CLI and runtime configuration; later state machine, recovery, and publishing
  validation/              Deterministic constraints before publishing
  adapters/                Adapters for test case generation and API automation
skills/                    Reserved directories for four project methods
examples/                  Sanitized examples
evals/                     Development data and evaluation entry points
tests/                     Scaffold and critical constraint tests
docs/                      Integration contracts, operating instructions, and acceptance records
```

The directories use the six Python package names from the plan. Installing the project makes the packages under `src/` available without manually changing `PYTHONPATH`.

## Runtime data

By default, `business-context init` creates `sources/`, `drafts/`, `packages/`, and `runs/` under `.data/` in the current working directory. The command can be run repeatedly without overwriting existing files. It initializes directories only; the fact database and agent checkpoint database will be created by their respective modules in later stages.

```powershell
uv run business-context init --data-dir D:\business-context-data
# Or use the environment variable; an explicit --data-dir takes precedence
$env:BUSINESS_CONTEXT_DATA_DIR = 'D:\business-context-data'
uv run business-context init
```

`.env.example` documents the environment variable and is not loaded automatically. `.data/`, `data/`, and local databases are ignored by Git. Custom runtime directories should be placed outside the repository. Real source materials, account credentials, and held-out evaluation answers should be stored in separate, access-controlled directories.

See the [architecture notes](docs/architecture.md) for the scope of future implementation and the [development roadmap](docs/development.md) for planned stages.
