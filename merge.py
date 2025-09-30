# Data consolidation script for merging multiple Excel files into a single dataset
# Takes individual page files from wine scraping and combines them into one master file
import pandas as pd  # For DataFrame operations and Excel file handling
import os  # For file system operations and path manipulation

def merge_excel_files(input_folder="data/pages", output_file="data/all_wines.xlsx"):
    """
    Merges multiple Excel files from a directory into a single consolidated Excel file.
    Removes duplicate entries based on vintage_id to ensure data integrity.
    
    Args:
        input_folder (str): Path to directory containing Excel files to merge
        output_file (str): Path for the consolidated output Excel file
    
    Returns:
        None: Saves merged data to specified output file
    """
    # Initialize list to store all DataFrames from individual files
    all_data = []
    
    # Iterate through all files in the input directory
    for file_name in os.listdir(input_folder):
        # Process only Excel files (skip any other file types)
        if file_name.endswith(".xlsx"):
            # Construct full file path
            file_path = os.path.join(input_folder, file_name)
            print(f"Reading {file_name}")
            # Load Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)
            # Add DataFrame to our collection
            all_data.append(df)

    # Combine all DataFrames vertically (stack rows from all files)
    # ignore_index=True creates a new continuous index for the merged data
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicate wine entries based on vintage_id
    # This handles cases where the same wine appears in multiple scraped pages
    # inplace=True modifies the DataFrame directly without creating a copy
    merged_df.drop_duplicates(subset=["vintage_id"], inplace=True)

    # Ensure the output directory exists before saving the file
    # exist_ok=True prevents errors if the directory already exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the consolidated DataFrame to Excel file
    # index=False prevents pandas from saving row indices as a column
    merged_df.to_excel(output_file, index=False)
    
    # Print summary statistics about the merge operation
    print(f"Merged {len(all_data)} files into {output_file}. Total rows: {len(merged_df)}")

# Execute the merge function with default parameters
# This will merge all Excel files from data/pages/ into data/all_wines.xlsx
merge_excel_files()
