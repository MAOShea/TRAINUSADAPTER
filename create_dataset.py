import json
import os
import random
import csv
import glob
import argparse

def create_dataset_from_csv(csv_file_path, set_name):
    """
    Create JSONL dataset files from CSV and widget code files.
    
    Args:
        csv_file_path: Path to the widget_processing_results.csv file
        set_name: Name of the dataset folder to create under datasets/
    """
    
    # Create dataset directory in current project
    dataset_dir = f'datasets/{set_name}'
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Output file paths
    train_file = os.path.join(dataset_dir, 'train.jsonl')
    valid_file = os.path.join(dataset_dir, 'valid.jsonl')
    test_file = os.path.join(dataset_dir, 'test.jsonl')
    
    # Load CSV data
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"Loaded CSV with {len(rows)} rows")
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
        return
    
    # Filter for JSX widgets only
    jsx_widgets = [row for row in rows if row.get('PS_isJSX') == 'Y']
    print(f"Found {len(jsx_widgets)} JSX widgets")
    
    # Check required columns
    if not jsx_widgets:
        print("No JSX widgets found")
        return
    
    sample_row = jsx_widgets[0]
    if 'AI_prompt' not in sample_row:
        print("Error: 'AI_prompt' column not found in CSV")
        return
    
    if 'PS_widgetfoldername' not in sample_row:
        print("Error: 'PS_widgetfoldername' column not found in CSV")
        return
    
    # Process each widget
    data = []
    for row in jsx_widgets:
        widget_id = row['OS_widget_id']
        widget_folder = row['PS_widgetfoldername']
        
        # Read prompt from prompts folder
        prompt_file = f'prompts/{widget_id}.prompt'
        if not os.path.exists(prompt_file):
            print(f"Skipping {widget_id}: No prompt file found at {prompt_file}")
            continue
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"Skipping {widget_id}: Could not read prompt file: {e}")
            continue
        
        # Skip if no prompt content
        if not prompt:
            print(f"Skipping {widget_id}: Empty prompt file")
            continue
        
        # Get widget code from filesystem
        widget_path = os.path.join('downloads', widget_folder)
        if not os.path.exists(widget_path):
            print(f"Skipping {widget_id}: Widget folder not found at {widget_path}")
            continue
        
        # Find and concatenate all JSX files
        jsx_files = glob.glob(os.path.join(widget_path, '**/*.jsx'), recursive=True)
        if not jsx_files:
            print(f"Skipping {widget_id}: No JSX files found")
            continue
        
        # Concatenate JSX files
        code_parts = []
        for jsx_file in sorted(jsx_files):
            try:
                with open(jsx_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        # Add filename as comment for context
                        relative_path = os.path.relpath(jsx_file, widget_path)
                        code_parts.append(f"// {relative_path}\n{content}")
            except Exception as e:
                print(f"Warning: Could not read {jsx_file}: {e}")
        
        if not code_parts:
            print(f"Skipping {widget_id}: No readable JSX content")
            continue
        
        # Join all JSX files with line breaks
        code = '\n\n'.join(code_parts)
        
        data.append({
            'prompt': prompt,
            'code': code,
            'widget_id': widget_id
        })
    
    print(f"Processed {len(data)} widgets with valid prompts and code")
    
    if len(data) == 0:
        print("No valid data to process")
        return
    
    # Shuffle and split data
    random.shuffle(data)
    train_size = int(0.8 * len(data))
    valid_size = int(0.1 * len(data))
    
    train_data = data[:train_size]
    valid_data = data[train_size:train_size + valid_size]
    test_data = data[train_size + valid_size:]
    
    def write_jsonl(dataset, output_file):
        """Write dataset to JSONL file in chat format"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in dataset:
                json_entry = [
                    {'role': 'system', 'content': 'You are a helpful assistant generating React/JSX widgets for Übersicht.'},
                    {'role': 'user', 'content': entry['prompt']},
                    {'role': 'assistant', 'content': entry['code']}
                ]
                f.write(json.dumps(json_entry, ensure_ascii=False) + '\n')
    
    # Write datasets
    write_jsonl(train_data, train_file)
    write_jsonl(valid_data, valid_file)
    write_jsonl(test_data, test_file)
    
    print(f'Dataset created: {len(train_data)} train, {len(valid_data)} valid, {len(test_data)} test')
    print(f'Files written to: {dataset_dir}')

def main():
    parser = argparse.ArgumentParser(description='Create JSONL dataset from widget CSV and code files')
    parser.add_argument('--csv', required=True, help='Path to widget_processing_results.csv')
    parser.add_argument('--set', required=True, help='Dataset name (creates folder under /datasets)')
    
    args = parser.parse_args()
    
    create_dataset_from_csv(args.csv, args.set)

if __name__ == '__main__':
    main()
