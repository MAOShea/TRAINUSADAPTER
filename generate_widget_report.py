#!/usr/bin/env python3

def has_coffee_files(folder_path):
    """Check if any .coffee files exist in the given folder (recursively)."""
    import glob
    import os
    
    # Use glob to recursively search for .coffee files
    coffee_pattern = os.path.join(folder_path, '**', '*.coffee')
    coffee_files = glob.glob(coffee_pattern, recursive=True)
    
    return len(coffee_files) > 0

def main():
    """Generate a comprehensive CSV report from widget data, categories, and coffee detection results."""
    import json
    import csv
    import os
    import glob
    from urllib.parse import urlparse
    
    # Read the widget list JSON file
    with open('widget_list.json', 'r') as f:
        data = json.load(f)
    
    # Read the categories CSV file to create a lookup dictionary
    categories_csv_path = 'widget_categories_complete.csv'
    category_lookup = {}
    
    try:
        with open(categories_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                widget_id = row['id']
                category_lookup[widget_id] = {
                    'category': row['category'],
                    'secondary_category': row['secondary_category']
                }
        print(f"Loaded categories for {len(category_lookup)} widgets")
    except FileNotFoundError:
        print(f"Warning: Categories file not found at {categories_csv_path}")
        print("Categories will be set to 'Unknown'")
    except Exception as e:
        print(f"Warning: Error reading categories file: {e}")
        print("Categories will be set to 'Unknown'")
    
    # Read download status file
    download_status = {}
    try:
        with open('download_status.json', 'r') as f:
            download_status = json.load(f)
        print(f"Loaded download status for {len(download_status)} widgets")
    except FileNotFoundError:
        print("Warning: download_status.json not found")
        print("Coffee detection will be set to 'Unknown' for all widgets")
    except Exception as e:
        print(f"Warning: Error reading download status: {e}")
        print("Coffee detection will be set to 'Unknown' for all widgets")
    
    # Check for downloads directory
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        print(f"Warning: Downloads directory not found at {downloads_dir}")
        print("Coffee detection will be set to 'Unknown'")
    
    # Prepare CSV output file
    csv_filename = 'widget_processing_results.csv'
    csv_headers = ['widget_id', 'name', 'author', 'description', 'filename', 'download_url', 'category', 'secondary_category', 'iscoffee']
    
    # Process all widgets in the array
    widgets = data['widgets']
    csv_data = []
    
    for widget in widgets:
        widget_id = widget['id']
        name = widget.get('name', 'Unknown')
        author = widget.get('author', 'Unknown')
        description = widget.get('description', 'No description available')
        download_url = widget['downloadUrl']
        
        # Extract filename from URL
        parsed_url = urlparse(download_url)
        filename = parsed_url.path.split('/')[-1]
        if not filename.endswith('.zip'):
            filename = f"{widget_id}.zip"
        
        # Look up categories for this widget
        category = 'Unknown'
        secondary_category = 'Unknown'
        if widget_id in category_lookup:
            category = category_lookup[widget_id]['category']
            secondary_category = category_lookup[widget_id]['secondary_category']
        
        # Check for coffee files based on download status
        iscoffee = 'Unknown'
        if widget_id in download_status:
            if download_status[widget_id] == 'success':
                # Only check for coffee files if download was successful
                if os.path.exists(downloads_dir):
                    # Create folder name (remove .zip extension)
                    folder_name = filename[:-4] if filename.endswith('.zip') else filename
                    extract_path = os.path.join(downloads_dir, folder_name)
                    
                    if os.path.exists(extract_path):
                        if has_coffee_files(extract_path):
                            iscoffee = 'Y'
                            print(f"Found .coffee files in: {folder_name}")
                        else:
                            iscoffee = 'N'
                    else:
                        iscoffee = 'Extraction Failed'
                else:
                    iscoffee = 'Downloads Directory Missing'
            elif download_status[widget_id] == 'failed':
                iscoffee = 'Download Failed'
            else:
                iscoffee = 'Unknown Status'
        else:
            iscoffee = 'Not Attempted'
        
        # Add row to CSV data
        csv_data.append([widget_id, name, author, description, filename, download_url, category, secondary_category, iscoffee])
    
    # Write CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        writer.writerows(csv_data)
    
    print(f"Generated report for {len(widgets)} widgets")
    print(f"Results saved to: {csv_filename}")

if __name__ == "__main__":
    main()
