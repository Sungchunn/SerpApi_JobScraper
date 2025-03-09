import os
import csv
import pandas as pd
import numpy as np
from serpapi import GoogleSearch

# Configuration
output_dir = "/path/to/output" # Replace with download directory
raw_output_file = f"{output_dir}/All_Job_Listings.csv"
sorted_output_file = f"{output_dir}/Sorted_Job_Listings.csv"
final_output_file = f"{output_dir}/Updated_Job_Listings.csv"
API_KEY = "your-serpapi-key" # Replace with SerpApi API key

# Define search parameters
job_roles = [
    "Junior Data Analyst",
    "Entry-Level Data Analyst",
    "Data Analyst Remote Asia",
    "Junior Data Scientist",
    "Junior Data Analyst",
    "Business Intelligence Analyst",
    "Quantitative Analyst"
]

locations = [
    "Bangkok", "Remote", "Malaysia", 
    "Jakarta", "Singapore", "Philippines", 
    "Vietnam", "Taiwan", "Shanghai",
    "Seoul", "Tokyo", "Hong Kong", 
    "Beijing", "Shenzhen", "Hyderabad", 
    "Bangalore", "Kuala Lumpur", "Ho Chi Minh City"
]

def search_jobs(query, location):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": API_KEY  
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])
    if not jobs:
        print(f"No jobs found for query '{query}' in '{location}'.")
        return []

    print(f"Found {len(jobs)} jobs for query '{query}' in '{location}'.")
    return jobs

def update_csv(new_jobs, source, existing_jobs):
    with open(raw_output_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        new_count = 0
        for job in new_jobs:
            job_link = job.get('job_id', 'N/A')
            if job_link not in existing_jobs:  # Check for duplicates
                writer.writerow([
                    job.get('title', 'N/A'),
                    job.get('company_name', 'N/A'),
                    job.get('location', 'N/A'),
                    job.get('detected_extensions', {}).get('posted_at', 'N/A'),
                    job_link,
                    source
                ])
                existing_jobs.add(job_link)
                new_count += 1
    print(f"Appended {new_count} new jobs from {source}.")
    return existing_jobs

def extract_days_ago(posted):
    if pd.isna(posted):
        return np.nan
    elif "hour" in posted or "minute" in posted:
        return 0  
    elif "day" in posted:
        return int(posted.split()[0])  
    else:
        return np.nan

def sort_job_listings():
    print("Sorting job listings by posting date...")
    df = pd.read_csv(raw_output_file)
    df["Days_Ago"] = df["Posted"].apply(extract_days_ago)
    df_sorted = df.sort_values(by="Days_Ago", ascending=True)
    df_sorted = df_sorted.drop(columns=["Days_Ago"])
    df_sorted.to_csv(sorted_output_file, index=False)
    print(f"Sorted job listings saved at: {sorted_output_file}")
    return df_sorted

def create_search_links(df):
    print("Creating search links for job listings...")
    df["Full_Link"] = "https://www.google.com/search?q=" + df["Title"].str.replace(" ", "+") + "+job+" + df["Company"].str.replace(" ", "+")
    df = df.drop(columns=["Link"])
    df.to_csv(final_output_file, index=False)
    print(f"Updated job listings saved at: {final_output_file}")
    return df

def main():

    print("Starting job search and data processing...")
    
    # Initialize CSV file if it doesn't exist
    if not os.path.exists(raw_output_file):
        os.makedirs(os.path.dirname(raw_output_file), exist_ok=True)
        with open(raw_output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Company", "Location", "Posted", "Link", "Source"])
    
    # Load existing job data to avoid duplicates
    existing_jobs = set()
    if os.path.exists(raw_output_file):
        df_existing = pd.read_csv(raw_output_file)
        if not df_existing.empty and "Link" in df_existing.columns:
            existing_jobs = set(df_existing["Link"].dropna())
    
    # Generate job search queries
    job_searches = [{"query": role, "location": loc} for role in job_roles for loc in locations]
    
    # Search for jobs and update CSV
    for search in job_searches:
        query = search["query"]
        location = search["location"]
        new_jobs = search_jobs(query, location)
        if new_jobs:
            existing_jobs = update_csv(new_jobs, f"{query} in {location}", existing_jobs)
    
    # Sort job listings by posting date
    sorted_df = sort_job_listings()
    
    # Create search links
    final_df = create_search_links(sorted_df)
    
    print("Job search and data processing complete!")
    print(f"Total job listings: {len(final_df)}")
    return final_df

if __name__ == "__main__":
    final_df = main()
    # Display sample of the final dataframe
    print("\nSample of processed job listings:")
    print(final_df.head())