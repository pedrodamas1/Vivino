# Web scraping script for extracting wine data from Vivino API
# Scrapes wine information including ratings, taste profiles, and geographical data
import requests  # For making HTTP requests to the Vivino API
import pandas as pd  # For data manipulation and Excel file creation
import time  # For adding delays between requests
import random  # For randomizing delay intervals
import os  # For file and directory operations

def scrape_red_wines_portugal(pages=50):
    """
    Scrapes wine data from Vivino's API for specified number of pages.
    
    Args:
        pages (int): Number of pages to scrape (default: 50)
    
    Returns:
        None: Saves data to Excel files in data/pages/ directory
    """
    # Create directory structure for storing scraped data
    folder_path = "data/pages"
    os.makedirs(folder_path, exist_ok=True)

    # Set headers to mimic a real browser request and avoid blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    # Loop through each page to scrape wine data
    for page in range(1, pages + 1):
        # Make API request to Vivino's explore endpoint
        response = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "page": page,  # Current page number
                "order": "asc",  # Sort order (ascending)
                "wine_type_ids[]": [1, 2, 3, 4, 7, 24],  # Wine type IDs for filtering specific types
            },
            headers=headers
        )

        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Extract wine matches from the JSON response
                wines = response.json()["explore_vintage"]["matches"]
                # Stop scraping if no wines are found on current page
                if not wines:
                    print("No more wines found. Stopping.")
                    break

                # Initialize list to store data for current page
                page_results = []
                # Process each wine in the current page
                for wine in wines:
                    # Extract taste profile attributes with error handling
                    # These attributes might not exist for all wines
                    try:
                        acidity = wine['vintage']['wine']['taste']['structure']['acidity']
                    except Exception as e:
                        acidity = None
                    try:
                        fizziness = wine['vintage']['wine']['taste']['structure']['fizziness']
                    except Exception as e:
                        fizziness = None
                    try:
                        intensity = wine['vintage']['wine']['taste']['structure']['intensity']
                    except Exception as e:
                        intensity = None
                    try:
                        sweetness = wine['vintage']['wine']['taste']['structure']['sweetness']
                    except Exception as e:
                        sweetness = None
                    try:
                        tannin = wine['vintage']['wine']['taste']['structure']['tannin']
                    except Exception as e:
                        tannin = None
                    
                    # Create a dictionary with all wine data for the current wine
                    page_results.append({
                        # Vintage-specific data
                        "vintage_id": wine['vintage']['id'],
                        "ratings_count": wine['vintage']['statistics']['ratings_count'],
                        "ratings_average": wine['vintage']['statistics']['ratings_average'],
                        # Wine-level statistics (aggregated across all vintages)
                        "wine_ratings_count": wine['vintage']['statistics']['wine_ratings_count'],
                        "wine_ratings_average": wine['vintage']['statistics']['wine_ratings_average'],
                        # Basic wine information
                        "wine_id": wine['vintage']['wine']['id'],
                        "wine_name": wine['vintage']['wine']['name'],
                        "wine_type_id": wine['vintage']['wine']['type_id'],
                        # Geographic information
                        "region_name": wine['vintage']['wine']['region']['name'],
                        "country_name": wine['vintage']['wine']['region']['country']['name'],
                        "winery_name": wine['vintage']['wine']['winery']['name'],
                        # Taste profile attributes
                        "acidity": acidity,
                        "fizziness": fizziness,
                        "intensity": intensity,
                        "sweetness": sweetness,
                        "tannin": tannin,
                    })
                    
                    # Commented out: Debug code for saving individual wine JSON data
                    # import json
                    # with open("wine.json", "w", encoding="utf-8") as file:
                    #     json.dump(wine, file, indent=4, ensure_ascii=False)

                # Convert the collected data to a pandas DataFrame
                df = pd.DataFrame(page_results)
                # Create file path for the current page's Excel file
                file_path = os.path.join(folder_path, f"page_{page}.xlsx")
                # Save DataFrame to Excel file
                df.to_excel(file_path, index=False)

                print(f"Page {page} scraped: {len(wines)} wines (saved to {file_path})")

            except KeyError as e:
                # Handle cases where expected JSON keys are missing
                print(f"Missing key: {e}")
        else:
            # Handle HTTP request failures
            print(f"Failed to fetch page {page}, status code: {response.status_code}")

        # Add random delay between requests to be respectful to the server
        # and avoid getting blocked
        time.sleep(random.uniform(1, 3))

    print(f"Scraping completed. Pages saved in '{folder_path}'")

# Execute the scraping function for 400 pages
# This will create Excel files for each page in the data/pages/ directory
scrape_red_wines_portugal(pages=400)
