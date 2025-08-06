# ChEMBL Molecular Weight Enrichment

This project provides simple Python scripts to:

1. Fetch molecular weight data from the ChEMBL API based on ChEMBL IDs.
2. Split large CSV files into smaller parts for easier processing.

## Files

- `chembl_tools.py`: Contains two main functions:
  - `enrich_with_molecular_weight`: Adds molecular weight to ChEMBL IDs in a CSV file.
  - `split_csv_file`: Splits a CSV file into multiple smaller files.

## Requirements

- Python 3.7 or newer
- `pandas`, `requests`

Install requirements using:

