#!/usr/bin/env python3
"""Download source data files specified in download.yaml."""

import shutil
import urllib.request
from pathlib import Path

import yaml

# Browser-like User-Agent to avoid 403 blocks from some servers
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def download_file(url: str, local_path: Path) -> None:
    """Download a file with browser-like headers to avoid bot blocking."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        with open(local_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)


def download_files():
    """Download all files specified in download.yaml."""
    with open("download.yaml") as f:
        config = yaml.safe_load(f)

    downloads = config.get("downloads", [])
    if not downloads:
        print("No downloads configured in download.yaml")
        return

    for item in downloads:
        url = item["url"]
        local_name = item["local_name"]
        local_path = Path(local_name)

        # Create parent directories if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if local_path.exists():
            print(f"Skipping {local_name} (already exists)")
            continue

        print(f"Downloading {url} -> {local_name}")
        download_file(url, local_path)
        print(f"  Downloaded {local_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    download_files()
