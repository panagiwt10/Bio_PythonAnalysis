import pandas as pd
import requests
import time
import os

# === Συνάρτηση για ανάκτηση ChEMBL δεδομένων(βαση του chemb_id) ===
def fetch_chembl_data(drug_name):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search?q={drug_name}"
    headers = {"Accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None
        results = res.json()
        if results['page_meta']['total_count'] == 0:
            return None
        chembl_id = results['molecules'][0]['molecule_chembl_id']

        # Δεύτερο αίτημα για λεπτομέρειες
        info_url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
        info_res = requests.get(info_url, headers=headers, timeout=10)
        if info_res.status_code != 200:
            return None
        info = info_res.json()
        return {
            "chembl_id": chembl_id,
            "molecular_weight": info.get("molecular_weight"),
            "inchi": info.get("molecule_structures", {}).get("standard_inchi"),
            "smiles": info.get("molecule_structures", {}).get("canonical_smiles"),
            "inchi_key": info.get("molecule_structures", {}).get("standard_inchi_key")

        }
    except Exception as e:
        print(f"❌ Σφάλμα ChEMBL για {drug_name}: {e}")
        return None

# === Έλεγχος εγκυρότητας ονόματος φαρμάκου ===
def is_valid_drug_name(name):
    if not isinstance(name, str):
        return False
    name = name.lower()
    if "fda" in name or "anda" in name or ":" in name:
        return False
    return True

# === Κύρια συνάρτηση για επεξεργασία αρχείου chunk ===
def process_clean_drug_chunk(input_file):
    print(f"\n📂 Επεξεργασία αρχείου: {input_file}")
    df = pd.read_excel(input_file)
    unique_names = df["drug_name"].dropna().str.strip().str.upper().unique()


    results = []

    for i, name in enumerate(unique_names, start=1):
        print(f"🔍 ({i}/{len(unique_names)}) {name}")
        result_row = {"drug_claim_name": name}

        if not is_valid_drug_name(name):
            print(" ⚠️ Αγνόηση λόγω ακατάλληλου ονόματος")
            results.append(result_row)
            continue

        chembl_data = fetch_chembl_data(name)
        if chembl_data:
            print(f" ✅ Βρέθηκε ChEMBL: {chembl_data['chembl_id']}")
            result_row.update(chembl_data)
        else:
            print(" ❌ Δεν βρέθηκε ChEMBL")

        results.append(result_row)
        time.sleep(1)

    enriched_df = pd.DataFrame(results)

    # === Αποθήκευση enriched αρχείου ===
    output_file = os.path.splitext(input_file)[0] + "_enriched.xlsx"
    enriched_df.to_excel(output_file, index=False)
    print(f"\n💾 Αποθηκεύτηκε enriched αρχείο: {output_file}")

#put it in a different jupyter if need be 
process_clean_drug_chunk("your_excel_file.xlsx")
