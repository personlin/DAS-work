"""Command-line helpers for DAS OpenDATA analysis."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

from rich.console import Console

from das_opendata_analysis.environment import configure_local_cache

console = Console()


def _read_contents(spool: Any) -> Any:
    """Return the DASCore spool contents table."""
    if hasattr(spool, "get_contents"):
        return spool.get_contents()
    msg = "The DASCore spool does not expose get_contents()."
    raise RuntimeError(msg)


def _index_path_for(data_path: Path) -> Path:
    """Return a deterministic project-local DASCore index path for a data path."""
    cache_root = configure_local_cache()
    index_root = cache_root / "dascore" / "indexes"
    index_root.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(str(data_path.resolve()).encode("utf-8")).hexdigest()[:16]
    return index_root / f"{digest}.h5"


def scan_dataset(path: Path, output: Path | None, update_index: bool) -> int:
    """Build an inventory for a DAS dataset and optionally save it to CSV."""
    configure_local_cache()
    import dascore as dc

    if not path.exists():
        console.print(f"[red]Input path does not exist:[/] {path}")
        return 2

    spool_kwargs = {"index_path": _index_path_for(path)} if path.is_dir() else {}
    spool = dc.spool(path, **spool_kwargs)
    if update_index and hasattr(spool, "update"):
        spool = spool.update()

    contents = _read_contents(spool)
    patch_count = len(contents)

    console.print(f"[green]DASCore version:[/] {dc.__version__}")
    console.print(f"[green]Input path:[/] {path}")
    console.print(f"[green]Patches indexed:[/] {patch_count}")

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        contents.to_csv(output, index=False)
        console.print(f"[green]Inventory written:[/] {output}")

    if patch_count:
        console.print(contents.head(min(5, patch_count)).to_string(index=False))

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="das-opendata-scan",
        description="Inventory a DAS OpenDATA directory with DASCore.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="data/raw",
        type=Path,
        help="DAS data file or directory to inventory. Defaults to data/raw.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("outputs/inventory.csv"),
        help="CSV path for the generated metadata inventory.",
    )
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip DASCore spool index refresh.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return scan_dataset(
        path=args.path,
        output=args.output,
        update_index=not args.no_update,
    )
