import pandas as pd
import requests
import time

def resolve_anda_to_generic(anda_id):
    url = f"https://api.fda.gov/drug/drugsfda.json?search=application_number:ANDA{anda_id}"
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"⚠️ FDA API error για ANDA{anda_id}")
            return None
        data = res.json()
        if "results" not in data:
            return None
        return data["results"][0]["products"][0]["active_ingredients"][0]["name"]
    except Exception as e:
        print(f"❌ Σφάλμα στο FDA API για ANDA{anda_id}: {e}")
        return None

def fetch_chembl_data(drug_name):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search?q={drug_name}"
    headers = {"Accept": "application/json"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None
        results = res.json()
        if results['page_meta']['total_count'] == 0:
            return None
        chembl_id = results['molecules'][0]['molecule_chembl_id']
        info_url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
        info_res = requests.get(info_url, headers=headers)
        if info_res.status_code != 200:
            return None
        info = info_res.json()
        return {
            "chembl_id": chembl_id,
            "molecular_weight": info.get("molecular_weight"),
            "inchi": info.get("molecule_structures", {}).get("standard_inchi"),
            "inchi_key": info.get("molecule_structures", {}).get("standard_inchi_key")
        }
    except Exception as e:
        print(f"❌ Σφάλμα στο ChEMBL για {drug_name}: {e}")
        return None

# === Φόρτωση του κύριου dataset ===
df = pd.read_excel("drugs.xlsx")
fda_df = df[df["normalized_drug_name"].str.contains("anda:", case=False, na=False)].copy()

print(f"🔎 Βρέθηκαν {len(fda_df)} εγγραφές τύπου ANDA")

results = []
for idx, row in fda_df.iterrows():
    raw_name = row["normalized_drug_name"]
    anda_number = raw_name.split("anda:")[-1].strip()

    print(f"\n🔍 Αναζήτηση για ANDA {anda_number} ({idx+1}/{len(fda_df)})")

    generic_name = resolve_anda_to_generic(anda_number)
    result_row = row.to_dict()
    result_row["resolved_generic_name"] = generic_name

    if generic_name:
        chembl_data = fetch_chembl_data(generic_name)
        if chembl_data:
            print(f"✅ Βρέθηκε ChEMBL: {chembl_data['chembl_id']}")
            result_row.update(chembl_data)
        else:
            print("❌ Δεν βρέθηκε ChEMBL")
    else:
        print("❌ Δεν βρέθηκε generic name από FDA")

    results.append(result_row)
    time.sleep(1)

# === Αποθήκευση των αποτελεσμάτων ===
output_df = pd.DataFrame(results)
output_df.to_excel("resolved_anda_with_chembl.xlsx", index=False)
print("\n✅ Ολοκληρώθηκε! Αποθηκεύτηκαν στο resolved_anda_with_chembl.xlsx")
