# string-ingest

This is a Koza ingest repository for transforming STRING DB protein-protein interaction data into Biolink model format.

## Project Structure

- `download.yaml` - Configuration for downloading source data (14 species + entrez mapping)
- `src/` - Transform code and configuration
  - `protein_links.py` - Transform code for protein links
  - `protein_links.yaml` - Koza config for protein links transform
  - `entrez_2_string.yaml` - Mapping file config for Entrez to STRING ID mapping
  - `versions.py` - Per-ingest upstream version fetcher (consumed by `just metadata`)
- `scripts/` - Utility scripts (download, preprocessing, plus `write_metadata.py` which emits `output/release-metadata.yaml`)
- `tests/` - Unit tests for transforms
- `output/` - Generated nodes and edges (gitignored)
  - `release-metadata.yaml` - Per-build manifest of upstream sources, versions, artifacts (kozahub-metadata-schema)
- `data/` - Downloaded source data (gitignored)

## Key Commands

- `just download` - Download source data
- `just transform-all` - Run all transforms
- `just transform protein_links` - Run protein links transform
- `just metadata` - Emit `output/release-metadata.yaml`
- `just test` - Run tests

## Data Sources

- STRING DB protein links for 14 species
- Entrez to STRING protein ID mapping file

## Release Metadata

Every kozahub ingest emits an `output/release-metadata.yaml` describing the upstream sources, their versions, the artifacts produced, and the versions of build-time tools. This file is the contract monarch-ingest reads to assemble the merged knowledge graph's release receipt.

`src/versions.py` is the only per-ingest piece — it implements `get_source_versions()` returning a list of SourceVersion dicts. The `kozahub_metadata_schema` package provides reusable fetchers for the common patterns (HTTP Last-Modified, GitHub releases, URL-path regex, file-header parsing). The boilerplate (transform-content hashing, tool versions, build_version composition, yaml emission) is handled by `scripts/write_metadata.py`.

The `kozahub-metadata-schema` repo is expected as a sibling checkout (path-dep). Switch to a git or PyPI dep once published.

## Output

- `string_protein_links_edges.tsv` - Pairwise gene-to-gene interactions

## Notes

- Large data volume: 14 species files
- Uses combined_score > 700 filter to reduce output
- Removes duplicate inverse pairs (A-B and B-A)
- Maps STRING protein IDs to NCBIGene IDs via Entrez mapping
