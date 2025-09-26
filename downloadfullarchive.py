#!/usr/bin/env python3

def main():
    """Main entry point for the download full archive script."""
    import json
    import os
    import requests
    import zipfile
    import argparse
    import sys
    from urllib.parse import urlparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download and extract widget archives')
    parser.add_argument('--widgets', type=str, help='Comma-separated list of widget IDs to download')
    parser.add_argument('--widget-file', type=str, help='File containing widget IDs to download (one per line)')
    args = parser.parse_args()
    
    # Create downloads directory if it doesn't exist
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    # Read the widget list JSON file
    with open('widget_list.json', 'r') as f:
        data = json.load(f)
    
    # Get all widgets
    all_widgets = data['widgets']
    
    # Initialize download status tracking
    download_status = {}
    
    # Validate and filter widgets if specified
    if args.widgets or args.widget_file:
        if args.widgets and args.widget_file:
            print("ERROR: Cannot specify both --widgets and --widget-file")
            sys.exit(1)
        
        if args.widgets:
            specified_ids = [wid.strip() for wid in args.widgets.split(',')]
        else:  # args.widget_file
            try:
                with open(args.widget_file, 'r') as f:
                    specified_ids = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"ERROR: Widget file not found: {args.widget_file}")
                sys.exit(1)
        
        available_ids = {widget['id'] for widget in all_widgets}
        invalid_ids = [wid for wid in specified_ids if wid not in available_ids]
        
        if invalid_ids:
            print(f"ERROR: The following widget IDs were not found in widget_list.json:")
            for wid in invalid_ids:
                print(f"  - {wid}")
            print(f"Available widget IDs: {len(available_ids)} total")
            sys.exit(1)
        
        # Filter to only specified widgets
        widgets = [w for w in all_widgets if w['id'] in specified_ids]
        print(f"Filtering to {len(widgets)} specified widgets")
    else:
        widgets = all_widgets
        print(f"Processing all {len(widgets)} widgets from widget_list.json")
    
    for widget in widgets:
        download_url = widget['downloadUrl']
        widget_id = widget['id']
        
        # Extract filename from URL
        parsed_url = urlparse(download_url)
        filename = os.path.basename(parsed_url.path)
        if not filename.endswith('.zip'):
            filename = f"{widget_id}.zip"
        
        file_path = os.path.join(downloads_dir, filename)
        
        # Download the ZIP file
        download_success = False
        try:
            response = requests.get(download_url)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
            
            # Unzip the file immediately after download
            try:
                # Create folder name (remove .zip extension)
                folder_name = filename[:-4] if filename.endswith('.zip') else filename
                extract_path = os.path.join(downloads_dir, folder_name)
                
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                print(f"Extracted: {folder_name}")
                download_success = True
                
            except Exception as e:
                print(f"Failed to extract {filename}: {e}")
                download_success = False
            
        except Exception as e:
            print(f"Failed to download {widget_id}: {e}")
            download_success = False
        
        # Record download status
        download_status[widget_id] = "success" if download_success else "failed"
    
    # Save download status to JSON file
    with open('download_status.json', 'w') as f:
        json.dump(download_status, f, indent=2)
    
    # Print summary
    success_count = sum(1 for status in download_status.values() if status == "success")
    failed_count = sum(1 for status in download_status.values() if status == "failed")
    
    print(f"Processed {len(widgets)} widgets")
    print(f"Successfully downloaded: {success_count}")
    print(f"Failed to download: {failed_count}")
    print(f"Download status saved to: download_status.json")

if __name__ == "__main__":
    main()

