import time
import os
import ssl
import pandas as pd
from Bio import Entrez
from datetime import datetime, timedelta

# Fix: SSL Certificate Verification Bypass
ssl._create_default_https_context = ssl._create_unverified_context

def get_date_ranges(start_year, end_year):
    """Generates monthly date ranges for the sliding window."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    ranges = []
    current = start_date
    while current < end_date:
        next_month = (current + timedelta(days=32)).replace(day=1)
        ranges.append((current.strftime("%Y/%m/%d"), (next_month - timedelta(days=1)).strftime("%Y/%m/%d")))
        current = next_month
    return ranges

def fetch_large_pulmonary_dataset(email, start_year=2020, end_year=2026, api_key=None):
    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key
    
    all_records = []
    big_5_mapping = {
        'Neoplasm': ['Lung Neoplasms', 'Carcinoma, Non-Small-Cell Lung'],
        'Infection': ['Respiratory Tract Infections', 'Pneumonia', 'COVID-19', 'Tuberculosis'],
        'Obstructive': ['Lung Diseases, Obstructive', 'Asthma', 'Pulmonary Disease, Chronic Obstructive'],
        'Vascular': ['Hypertension, Pulmonary', 'Pulmonary Embolism'],
        'Injury': ['Respiratory Distress Syndrome', 'Acute Lung Injury']
    }

    date_chunks = get_date_ranges(start_year, end_year)
    
    for start, end in date_chunks:
        print(f"Fetching: {start} to {end}...")
        query = f"Respiratory Tract Diseases[MeSH] AND ({start}[PDAT] : {end}[PDAT])"
        
        try:
            # 1. Search for IDs using the History Server optimization
            search_handle = Entrez.esearch(db="pubmed", term=query, usehistory="y", retmax=10000)
            search_results = Entrez.read(search_handle)
            search_handle.close()
            
            count = int(search_results["Count"])
            if count == 0: 
                print(f"No records found for {start}-{end}")
                continue
            
            # 2. Fetch records in batches
            fetch_handle = Entrez.efetch(
                db="pubmed", 
                webenv=search_results["WebEnv"], 
                query_key=search_results["QueryKey"],
                retmode="xml"
            )
            records = Entrez.read(fetch_handle)
            fetch_handle.close()

            # 3. Process and Multi-Label
            for article in records.get('PubmedArticle', []):
                medline = article['MedlineCitation']
                # Join abstract fragments safely
                abstract_nodes = medline['Article'].get('Abstract', {}).get('AbstractText', [])
                abstract = " ".join([str(text) for text in abstract_nodes])
                
                mesh_list = [str(m['DescriptorName']) for m in medline.get('MeshHeadingList', [])]
                
                labels = {group: (1 if any(term in mesh_list for term in terms) else 0) 
                          for group, terms in big_5_mapping.items()}
                
                all_records.append({
                    'pmid': str(medline['PMID']),
                    'year': start[:4],
                    'abstract': abstract,
                    **labels
                })
            
            # Respect rate limits
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"Error in range {start}-{end}: {e}")
            time.sleep(1) # Pause before retry
            continue

    df = pd.DataFrame(all_records)
    
    # Save to /dataset folder
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{start_year}-{end_year}_Pulmonary_Research.csv"
    filepath = os.path.join(output_dir, filename)
    
    df.to_csv(filepath, index=False)
    print(f"Dataset saved successfully to {filepath}")
    
    return df