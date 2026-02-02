import json
import os
import random
import csv
import glob
import argparse
import sys
import training_config
from training_config import TOOL_DEFINITION

# Rough token estimation: ~4 chars per token for code/text (matches evaluate_training_data_size.py)
CHARS_PER_TOKEN = 4

def estimate_tokens(text_length, chars_per_token=CHARS_PER_TOKEN):
    """Estimate token count from character length"""
    return int(text_length / chars_per_token)

def truncate_code_to_tokens(code, max_tokens):
    """
    Truncate widget code to fit within max_tokens limit.
    Truncates from the end, preserving the beginning.
    """
    if max_tokens <= 0:
        return ""
    
    max_chars = max_tokens * CHARS_PER_TOKEN
    if len(code) <= max_chars:
        return code
    
    # Truncate, but try to break at a newline if possible
    truncated = code[:max_chars]
    last_newline = truncated.rfind('\n')
    
    # If we find a newline in the last 10% of truncation, use it for cleaner break
    if last_newline > max_chars * 0.9:
        return code[:last_newline]
    
    return truncated

def load_strategy(strategy_file='training_data_strategy.json'):
    """
    Load strategy recommendations from JSON file.
    Returns dict mapping widget_id to strategy entry, or empty dict if file doesn't exist.
    """
    if not os.path.exists(strategy_file):
        return {}
    
    try:
        with open(strategy_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('strategy', {})
    except Exception as e:
        print(f"Warning: Could not load strategy file {strategy_file}: {e}")
        return {}
        
# Extraction functions removed - now using complete widget code as jsxContent

def resolve_system_prompt(prompt_name):
    """Resolve a system prompt string by name from training_config."""
    if not hasattr(training_config, prompt_name):
        available = [
            name for name in dir(training_config)
            if name.startswith('systemPrompt')
        ]
        available_display = ', '.join(sorted(available)) or '(none)'
        raise ValueError(
            f"Unknown system prompt '{prompt_name}'. "
            f"Available prompts: {available_display}"
        )
    prompt_value = getattr(training_config, prompt_name)
    if not isinstance(prompt_value, str):
        raise ValueError(
            f"System prompt '{prompt_name}' is not a string."
        )
    return prompt_value


def create_dataset_from_csv(
    csv_file_path,
    set_name,
    strategy_file='training_data_strategy.json',
    system_prompt_name='systemPrompt_v6',
):
    """
    Create JSONL dataset files from CSV and widget code files.
    
    Args:
        csv_file_path: Path to the widget_processing_results.csv file
        set_name: Name of the dataset folder to create under datasets/
        strategy_file: Path to strategy JSON file (default: training_data_strategy.json)
    """
    
    # Resolve system prompt once
    system_prompt = resolve_system_prompt(system_prompt_name)

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
    
    # Load strategy file if it exists
    strategy = load_strategy(strategy_file)
    if strategy:
        print(f"Loaded strategy file: {len(strategy)} widgets have strategy recommendations")
    else:
        print("No strategy file found - processing all widgets without exclusions/truncations")
    
    # Process each widget
    data = []
    excluded_count = 0
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
        
        # Apply strategy if available
        if widget_id in strategy:
            widget_strategy = strategy[widget_id]
            action = widget_strategy.get('action', 'keep')
            
            if action == 'exclude':
                excluded_count += 1
                reason = widget_strategy.get('reason', 'Strategy recommends exclusion')
                print(f"Skipping {widget_id}: {reason}")
                continue
        
        data.append({
            'prompt': prompt,
            'code': code,
            'widget_id': widget_id
        })
    
    print(f"Processed {len(data)} widgets with valid prompts and code")
    if excluded_count > 0:
        print(f"  Excluded: {excluded_count} widgets (exceeded token limit per strategy recommendations)")
    
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
    
    def validate_jsonl_file(file_path):
        """Validate that all lines in a JSONL file contain valid JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f'Error in {file_path}, line {i}: {e}')
                    sys.exit(1)
    
    def write_jsonl(dataset, output_file):
        """Write dataset to JSONL file in chat format with tools"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in dataset:
                # Generate a tool call ID
#                tool_call_id = f"call_{uuid.uuid4().hex[:16]}"
                
                # Create the arguments JSON object, then stringify it for the tool call
                arguments_obj = {
                    'jsxContent': entry['code']
                }
                arguments_json = json.dumps(arguments_obj, ensure_ascii=False)
                
                json_entry = [
                    {
                        'role': 'system', 
                        'content': system_prompt,
                        'tools': [TOOL_DEFINITION]
                    },
                    {'role': 'user', 'content': entry['prompt']},
                    {
                        'role': 'assistant',
                        'content': '',
                        'tool_calls': [
                            {
#                                'id': tool_call_id,
                                'type': 'function',
                                'function': {
                                    'name': 'WriteUbersichtWidgetToFileSystem',
                                    'arguments': arguments_json
                                }
                            }
                        ]
                    }
                ]
                f.write(json.dumps(json_entry, ensure_ascii=False) + '\n')
    
    # Write datasets
    write_jsonl(train_data, train_file)
    write_jsonl(valid_data, valid_file)
    write_jsonl(test_data, test_file)
    
    # Validate generated JSONL files
    print('Validating generated JSONL files...')
    validate_jsonl_file(train_file)
    validate_jsonl_file(valid_file)
    validate_jsonl_file(test_file)
    print('All lines valid!')
    
    print(f'Dataset created: {len(train_data)} train, {len(valid_data)} valid, {len(test_data)} test')
    print(f'Files written to: {dataset_dir}')

def main():
    parser = argparse.ArgumentParser(description='Create JSONL dataset from widget CSV and code files')
    parser.add_argument('--csv', required=True, help='Path to widget_processing_results.csv')
    parser.add_argument('--set', required=True, help='Dataset name (creates folder under /datasets)')
    parser.add_argument(
        '--strategy',
        default='training_data_strategy.json',
        help='Path to strategy JSON file for exclusions/truncations (default: training_data_strategy.json)',
    )
    parser.add_argument(
        '--system-prompt',
        default='systemPrompt_v6',
        help='Name of the system prompt string in training_config.py (default: systemPrompt_v6)',
    )
    
    args = parser.parse_args()
    
    create_dataset_from_csv(
        args.csv,
        args.set,
        args.strategy,
        system_prompt_name=args.system_prompt,
    )

if __name__ == '__main__':
    main()
