import os
import certifi
from dotenv import load_dotenv
from API.pubmed import fetch_large_pulmonary_dataset

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Configuration
EMAIL = os.getenv("EMAIL")
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    print("Starting Pulmonary Research Pulse Data Ingestion...")
    
    # This will automatically create the /dataset folder and save the CSV
    dataset = fetch_large_pulmonary_dataset(
        email=EMAIL, 
        start_year=2020, 
        end_year=2026, 
        api_key=API_KEY
    )
    
    print(f"Total records processed: {len(dataset)}")