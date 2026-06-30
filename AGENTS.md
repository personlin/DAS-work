# AGENTS.md

## Project Goal

Analyze Distributed Acoustic Sensing OpenDATA with DASCore while keeping the
workspace reproducible, data-provenanced, and lightweight enough for iterative
experiments.

## Environment

- Use `uv` for Python environment management.
- Primary setup command: `uv sync --extra dev --extra notebook`.
- Run Python commands through `uv run` unless the `.venv` is already activated.
- Local Python is expected to satisfy `requires-python >=3.10`.
- The project-level `sitecustomize.py` redirects package caches into `.cache/`
  so DASCore/Pint does not write to user-level AppData during sandboxed runs.

## Common Commands

```powershell
uv sync --extra dev --extra notebook
.\.venv\Scripts\das-opendata-scan.exe data/raw --output outputs/inventory.csv
.\.venv\Scripts\pytest.exe -p no:cacheprovider
.\.venv\Scripts\ruff.exe check --no-cache .
```

## Repository Layout

- `src/das_opendata_analysis/`: repeatable Python utilities and CLIs.
- `notebooks/`: exploratory notebooks; move stable logic into `src/`.
- `data/raw/`: original downloaded or mounted OpenDATA files.
- `data/processed/`: local derived data products.
- `outputs/`: generated figures, inventories, and reports.

## Data Rules

- Do not commit raw DAS data, processed data, large generated files, or secrets.
- Keep source URLs, download dates, license notes, and processing parameters with
  any analysis result that leaves the local machine.
- Prefer small metadata inventories in Git over bulky binary data.

## DASCore Conventions

- Prefer DASCore APIs (`dascore.spool`, patches, coords, attrs, and transforms)
  over ad hoc file parsing.
- Keep DASCore directory indexes under `.cache/dascore/`; do not write index
  files into `data/raw/` or mounted source-data directories.
- Preserve units, coordinate names, sampling rates, and time ranges in outputs.
- For repeatable workflows, add a CLI or module under `src/` instead of leaving
  the only implementation in a notebook.

## Change Guidance

- Keep changes scoped to the analysis workflow.
- Update `pyproject.toml` when dependencies or command entry points change.
- Add tests for stable helper functions; notebooks are not a substitute for
  tests around reusable code.
- Commit after each completed change set.
