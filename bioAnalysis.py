# Εγκατάσταση και Εισαγωγή των Βιβλιοθηκών
!pip install chembl_webresource_client pandas ipywidgets plotly

import pandas as pd
from chembl_webresource_client.new_client import new_client
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

# Λειτουργία για την Αναζήτηση Ενώσεων
def search_compounds(term):
    compound = new_client.molecule
    compound_query = compound.search(term)
    return pd.DataFrame.from_dict(compound_query)

# Λειτουργία για την Αναζήτηση Assays
def search_assays(term):
    assay = new_client.assay
    assay_query = assay.search(term)
    return pd.DataFrame.from_dict(assay_query)

# Αναζήτηση Ενώσεων με το Term 'liver toxicity'
compounds = search_compounds('liver toxicity')

# Έλεγχος και Εμφάνιση Αποτελεσμάτων για Ενώσεις
if not compounds.empty:
    print("Columns in compounds DataFrame:", compounds.columns)
    columns_to_display = ['molecule_chembl_id', 'molecule_type', 'pref_name']
    if 'standard_value' in compounds.columns:
        columns_to_display.append('standard_value')
        
    print("Compounds DataFrame:")
    display(compounds[columns_to_display])

    # Οπτικοποίηση του standard_value αν υπάρχει
    if 'standard_value' in compounds.columns:
        fig = px.histogram(compounds, x='standard_value', title='Distribution of Standard Values for Liver Toxicity')
        fig.show()
    else:
        print("No 'standard_value' column available for visualization.")

    # Αποθήκευση σε CSV
    compounds.to_csv("compounds_liver_toxicity.csv", index=False)
else:
    print("No data found for 'liver toxicity' in compounds.")

# Λήψη Δραστικοτήτων IC50 για το Target "hepatocytes"
target = new_client.target
target_query = target.search('hepatocytes')

if not target_query:
    print("No target found for 'hepatocytes'.")
else:
    selected_target = target_query[0]['target_chembl_id']
    
    # Φιλτράρισμα δραστικοτήτων για το IC50
    activity = new_client.activity
    res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
    activities_df = pd.DataFrame.from_dict(res)
    
    if not activities_df.empty:
        print("Activity DataFrame for IC50:")
        columns_to_display = ['molecule_chembl_id', 'standard_value', 'standard_units']
        display(activities_df[columns_to_display])
        
        # Οπτικοποίηση της κατανομής IC50 αν υπάρχει το 'standard_value'
        if 'standard_value' in activities_df.columns:
            fig = px.histogram(activities_df, x='standard_value', title='Distribution of IC50 Values for Hepatocytes')
            fig.show()

        # Αποθήκευση των δραστικοτήτων σε CSV
        activities_df.to_csv("activities_hepatocytes_IC50.csv", index=False)
    else:
        print("No activity data with IC50 for 'hepatocytes'.")

