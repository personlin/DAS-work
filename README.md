# DAS OpenDATA Analysis

This workspace is for analyzing Distributed Acoustic Sensing OpenDATA with
[DASCore](https://github.com/DASDAE/dascore).

## Environment

```powershell
uv sync --extra dev --extra notebook
```

Activate the virtual environment manually when needed:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quick checks:

```powershell
.\.venv\Scripts\python.exe -c "import dascore as dc; print(dc.__version__)"
.\.venv\Scripts\das-opendata-scan.exe --help
.\.venv\Scripts\pytest.exe -p no:cacheprovider
.\.venv\Scripts\ruff.exe check --no-cache .
```

This project installs a local `sitecustomize.py` that redirects Python package
caches used by DASCore/Pint into `.cache/` inside the workspace.

## Data Layout

- `data/raw/`: downloaded or mounted OpenDATA inputs. This is ignored by Git.
- `data/processed/`: derived local data products. This is ignored by Git.
- `notebooks/`: exploratory analysis.
- `outputs/`: reports, figures, inventories, and other generated artifacts.
- `src/das_opendata_analysis/`: repeatable analysis utilities.

## Inventory A Dataset

Put DAS data under `data/raw/`, then run:

```powershell
uv run das-opendata-scan data/raw --output outputs/inventory.csv
```

The scanner builds a DASCore spool, refreshes the local index when possible, and
writes a patch metadata inventory for review. DASCore directory indexes are kept
under `.cache/dascore/` so source data directories can remain read-only.
