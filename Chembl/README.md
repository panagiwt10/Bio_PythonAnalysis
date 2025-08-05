# 🧪 ChEMBL Compound Search & Analysis (bioPython_analysis.py)

Αυτό το project πραγματοποιεί αναζήτηση ενώσεων στο ChEMBL σχετικές με "liver toxicity", αποθηκεύει τα δεδομένα και δημιουργεί διαδραστικά γραφήματα για ανάλυση.

## 📋 Λειτουργίες
- 🔎 Αναζήτηση ενώσεων από τη βάση δεδομένων ChEMBL.
- 💾 Αποθήκευση αποτελεσμάτων σε αρχείο CSV.
- 📊 Οπτικοποίηση δεδομένων:
  - Pie chart για την κατανομή τύπων μορίων.
  - Bar chart με τις Top 10 ενώσεις βάσει ονόματος.
- 🎯 Φιλτράρισμα μόνο για Small Molecules.

## ⚙️ Απαιτήσεις
- Python 3.x
- Βιβλιοθήκες:
  ```bash
  pip install pandas chembl_webresource_client plotly
