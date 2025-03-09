A Python tool that scrapes job listings for data analyst positions across Asia using SerpAPI, then processes and organizes the data for easy access.

## Code explaination: 
1. Searching for various data-related job roles across multiple Asian locations
2. Collecting detailed job information including titles, companies, locations, and posting dates
3. Sorting jobs by recency and generating searchable links
4. Eliminating duplicate listings

## Requirements
- Python 3.6+
- pandas
- numpy
- serpapi


## Installation

1. Clone this repository
```
git clone https://github.com/your-username/jobscraper.git
cd jobscraper
```

2. Install required packages

```
pip install pandas numpy serpapi
```

3. Add your SerpAPI key to the script (or set up environment variables)

## Usage
Just run the main script:
```
python job_scraper.py
```