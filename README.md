# string-ingest

STRING DB protein links ingest - transforms protein-protein interaction data from STRING database into Biolink model format.

## Setup

```bash
just setup
```

## Usage

### Download source data

```bash
just download
```

### Run transforms

```bash
# Run all transforms
just transform-all

# Run specific transform
just transform <transform_name>
```

### Run tests

```bash
just test
```

## Data Sources

- STRING DB protein links (14 species)
- STRING DB Entrez to protein ID mappings

## Output

- `string_protein_links_edges.tsv` - Pairwise gene-to-gene interactions

## License

BSD-3-Clause
