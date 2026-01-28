# string-ingest

This is a Koza ingest repository for transforming STRING DB protein-protein interaction data into Biolink model format.

## Project Structure

- `download.yaml` - Configuration for downloading source data (14 species + entrez mapping)
- `src/` - Transform code and configuration
  - `protein_links.py` - Transform code for protein links
  - `protein_links.yaml` - Koza config for protein links transform
  - `entrez_2_string.yaml` - Mapping file config for Entrez to STRING ID mapping
- `scripts/` - Utility scripts (download, preprocessing)
- `tests/` - Unit tests for transforms
- `output/` - Generated nodes and edges (gitignored)
- `data/` - Downloaded source data (gitignored)

## Key Commands

- `just download` - Download source data
- `just transform-all` - Run all transforms
- `just transform protein_links` - Run protein links transform
- `just test` - Run tests

## Data Sources

- STRING DB protein links for 14 species
- Entrez to STRING protein ID mapping file

## Output

- `string_protein_links_edges.tsv` - Pairwise gene-to-gene interactions

## Notes

- Large data volume: 14 species files
- Uses combined_score > 700 filter to reduce output
- Removes duplicate inverse pairs (A-B and B-A)
- Maps STRING protein IDs to NCBIGene IDs via Entrez mapping
