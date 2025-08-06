import pandas as pd
import requests
import time
import os
import math

# 1. Συνάρτηση για ανάκτηση μοριακού βάρους από ChEMBL
def fetch_molecular_weight(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
    headers = {"Accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        mw = data.get("molecule_properties", {}).get("full_mwt")
        return float(mw) if mw else None
    except Exception as e:
        print(f"Σφάλμα για {chembl_id}: {e}")
        return None

# 2. Συνάρτηση για εμπλουτισμό του αρχείου CSV
def enrich_with_molecular_weight(input_file):
    print(f"Επεξεργασία αρχείου: {input_file}")
    
    df = pd.read_csv(input_file)
    df["ChEMBL_ID"] = df["ChEMBL_ID"].astype(str).str.strip().str.upper()

    weights = []
    for i, chembl_id in enumerate(df["ChEMBL_ID"], start=1):
        weight = fetch_molecular_weight(chembl_id)
        weights.append(weight)
        if weight is not None:
            print(f"({i}/{len(df)}) {chembl_id}: {weight}")
        else:
            print(f"({i}/{len(df)}) {chembl_id}: Not found")
        time.sleep(1)

    df["molecular_weight"] = weights
    output_file = os.path.splitext(input_file)[0] + "_weights_only.csv"
    df.to_csv(output_file, index=False)
    print(f"Ολοκληρώθηκε και αποθηκεύτηκε: {output_file}")

# 3. Συνάρτηση για διαχωρισμό CSV σε μικρότερα κομμάτια
def split_csv_file(input_file, lines_per_file=1000):
    print(f"Φόρτωση αρχείου: {input_file}")
    df = pd.read_csv(input_file)
    
    total = len(df)
    parts = math.ceil(total / lines_per_file)
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    
    for i in range(parts):
        start = i * lines_per_file
        end = start + lines_per_file
        part_df = df.iloc[start:end]
        
        output_filename = f"{base_filename}_part_{i+1}.csv"
        part_df.to_csv(output_filename, index=False)
        print(f"Αποθηκεύτηκε: {output_filename} ({len(part_df)} γραμμές)")

    print(f"Ολοκληρώθηκε το split σε {parts} αρχεία.")

# Εκτέλεση
# enrich_with_molecular_weight("your_csv.csv")
# split_csv_file("your_file_to_split.csv", lines_per_file=1000)
