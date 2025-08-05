# 🧬 FDA_autoScript.py

Το `FDA_autoScript.py` είναι ένα Python script που συνδυάζει δεδομένα από τον **FDA** και το **ChEMBL** για να εμπλουτίσει φαρμακευτικές εγγραφές τύπου `ANDA` με:

- το **γενόσημο όνομα** από το FDA API
- το **ChEMBL ID**, **μοριακό βάρος**, **InChI** και **InChI Key** από το ChEMBL API

---

## 🔍 Περιγραφή λειτουργίας

1. **Ανάγνωση Excel**: Διαβάζει αρχείο `drugs.xlsx` με στήλη `normalized_drug_name`.
2. **Εντοπισμός ANDA εγγραφών**: Φιλτράρει εγγραφές που περιέχουν `anda:` (case-insensitive).
3. **Ανάκτηση Generic Name**: Χρησιμοποιεί το [FDA Open API](https://open.fda.gov/) για να εξάγει το γενόσημο όνομα.
4. **Ανάκτηση ChEMBL Data**: Καλεί το [ChEMBL API](https://www.ebi.ac.uk/chembl/) και εξάγει:
   - `chembl_id`
   - `molecular_weight`
   - `standard_inchi`
   - `standard_inchi_key`
5. **Αποθήκευση Αποτελεσμάτων**: Τα enriched δεδομένα αποθηκεύονται σε `resolved_and_
