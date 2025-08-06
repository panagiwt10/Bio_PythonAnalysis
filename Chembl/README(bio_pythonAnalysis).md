# ChEMBL Drug Name Enrichment Script

This script enriches drug names with ChEMBL-related data by querying the [ChEMBL API](https://www.ebi.ac.uk/chembl/).

## 📌 What It Does

- Accepts an Excel file (`.xlsx`) with a `drug_name` column.
- Cleans and validates the drug names.
- For each valid drug name, retrieves the following from ChEMBL:
  - **ChEMBL ID**
  - **SMILES**
  - **InChI**
  - **InChI Key**
- Exports the enriched data to a new Excel file.

## 📥 Input Format

- The input Excel file **must** contain a column named:



- Each row should include one drug name.
- The script **automatically filters out**:
- Common metadata like `fda`, `anda`
- Names containing a colon `:` (e.g., `DrugX:Info`)

## 📤 Output

A new Excel file is created in the same directory as the input, with `_enriched.xlsx` appended to the filename.

The output includes the following columns:

- `drug_claim_name`
- `chembl_id`
- `molecular_weight`
- `inchi`
- `smiles`
- `inchi_key`

## 📦 Requirements

- Python 3.7 or newer  
- The following Python libraries:
- `pandas`
- `requests`
- `openpyxl`

Install the required packages using:

```bash
pip install pandas requests openpyxl

▶️ Usage
You can run the script in any Python environment (script or notebook). Example usage:
process_clean_drug_chunk("your_excel_file.xlsx")

eplace "your_excel_file.xlsx" with the path to your actual file.

⚠️ Notes
The script includes a 1-second delay between API calls to respect ChEMBL's rate limits.

Only the first ChEMBL match per drug name is used.

Drug names that are incomplete or invalid are skipped silently.
