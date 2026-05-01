"""Upstream source version fetcher for string-ingest.

STRING DB URLs encode the release version in their path
(e.g. `protein.links.detailed.v12.0`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kozahub_metadata_schema import (
    now_iso,
    urls_from_download_yaml,
    version_from_url_path,
)


INGEST_DIR = Path(__file__).resolve().parents[1]
DOWNLOAD_YAML = INGEST_DIR / "download.yaml"


def get_source_versions() -> list[dict[str, Any]]:
    urls = urls_from_download_yaml(DOWNLOAD_YAML)
    versioned = [u for u in urls if "protein.links.detailed.v" in u]
    version, method = version_from_url_path(
        versioned[0] if versioned else "", r"protein\.links\.detailed\.v(\d+\.\d+)"
    )
    return [
        {
            "id": "infores:string",
            "name": "STRING — Functional Protein Interaction Networks",
            "urls": urls,
            "version": version,
            "version_method": method,
            "retrieved_at": now_iso(),
        }
    ]
