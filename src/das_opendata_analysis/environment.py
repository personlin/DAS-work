"""Project-local runtime environment setup."""

from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Return the workspace root for this editable package."""
    return Path(__file__).resolve().parents[2]


def configure_local_cache() -> Path:
    """Redirect platformdirs cache lookups to a workspace-local cache directory."""
    cache_root = Path(os.environ.get("DAS_OPENDATA_CACHE_DIR", project_root() / ".cache"))
    cache_root.mkdir(parents=True, exist_ok=True)
    matplotlib_cache = cache_root / "matplotlib"
    matplotlib_cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(matplotlib_cache))

    try:
        import platformdirs
    except ImportError:
        return cache_root

    def user_cache_path(
        appname: str | None = None,
        appauthor: str | bool | None = None,
        version: str | None = None,
        opinion: bool = True,
        ensure_exists: bool = False,
    ) -> Path:
        del appauthor, opinion
        path = cache_root / (appname or "python")
        if version:
            path = path / version
        if ensure_exists:
            path.mkdir(parents=True, exist_ok=True)
        return path

    def user_cache_dir(
        appname: str | None = None,
        appauthor: str | bool | None = None,
        version: str | None = None,
        opinion: bool = True,
        ensure_exists: bool = False,
    ) -> str:
        return str(
            user_cache_path(
                appname=appname,
                appauthor=appauthor,
                version=version,
                opinion=opinion,
                ensure_exists=ensure_exists,
            )
        )

    platformdirs.user_cache_path = user_cache_path
    platformdirs.user_cache_dir = user_cache_dir
    return cache_root
