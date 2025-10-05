#!/usr/bin/env python3
"""
Inject AI categories into widget_processing_results.csv from widget_categorisation.json
"""

import csv
import json
import os

def inject_categories(csv_file='widget_processing_results.csv', json_file='widget_categorisation.json'):
    """
    Read categories from JSON file and inject them into the CSV file.
    
    Args:
        csv_file (str): Path to the CSV file to update
        json_file (str): Path to the JSON file containing categorizations
    """
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return False
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return False
    
    # Read categorizations from JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            categorizations = json.load(f)
        print(f"Loaded categorizations for {len(categorizations)} widgets")
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return False
    
    # Read existing CSV
    try:
        rows = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        print(f"Loaded CSV with {len(rows)} widgets")
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return False
    
    # Update rows with new categories
    updated_count = 0
    not_found_count = 0
    
    for row in rows:
        widget_id = row[0]  # OS_widget_id is column 0
        
        if widget_id in categorizations:
            primary, secondary = categorizations[widget_id]
            row[6] = primary   # AI_category (column 6)
            row[7] = secondary # AI_secondary_category (column 7)
            updated_count += 1
        else:
            not_found_count += 1
    
    # Write back to CSV
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Successfully updated CSV file")
    except Exception as e:
        print(f"Error writing {csv_file}: {e}")
        return False
    
    # Summary
    print(f"\nSummary:")
    print(f"  Updated: {updated_count} widgets")
    print(f"  Not found in categorizations: {not_found_count} widgets")
    print(f"  Total processed: {len(rows)} widgets")
    
    return True

def main():
    """Main function to run the category injection."""
    print("Starting category injection process...")
    
    success = inject_categories()
    
    if success:
        print("\n✅ Category injection completed successfully!")
    else:
        print("\n❌ Category injection failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
