#!/usr/bin/env python3
"""
Analyze all widgets in the downloads folder to identify their data sources.
"""

import os
import glob
import re
import json
from collections import defaultdict
from pathlib import Path

# Data source patterns to identify
DATA_SOURCE_PATTERNS = {
    'weather': [
        r'weather\.com',
        r'openweathermap',
        r'darksky',
        r'wunderground',
        r'wttr\.in',
        r'api\.weather',
        r'weather\.gov',
        r'forecast',
        r'temperature',
        r'humidity',
        r'weather',
        r'rain',
        r'snow',
        r'wind',
    ],
    'crypto': [
        r'bitcoin',
        r'btc',
        r'crypto',
        r'coinbase',
        r'binance',
        r'cryptocurrency',
        r'ethereum',
        r'eth',
        r'ltc',
        r'litecoin',
        r'marketcap',
        r'crypto.*price',
    ],
    'stock': [
        r'stock',
        r'nasdaq',
        r'nyse',
        r'yahoo.*finance',
        r'alpha.*vantage',
        r'iex',
        r'stock.*price',
        r'equity',
    ],
    'system': [
        r'exec\(|run\(|shell',
        r'cpu',
        r'memory|ram',
        r'disk',
        r'battery',
        r'uptime',
        r'load',
        r'network',
        r'process',
        r'istats',
        r'system',
        r'/usr/bin',
        r'/bin/',
    ],
    'calendar': [
        r'ical',
        r'calendar',
        r'\.ics',
        r'event',
        r'appointment',
        r'google.*calendar',
        r'outlook.*calendar',
    ],
    'email': [
        r'imap',
        r'email',
        r'mail',
        r'gmail',
        r'outlook',
        r'exchange',
        r'inbox',
    ],
    'github': [
        r'github\.com/api',
        r'api\.github\.com',
        r'github.*api',
        r'github.*issue',
        r'github.*notification',
        r'github.*activity',
        r'github.*repo',
    ],
    'gitlab': [
        r'gitlab\.com/api',
        r'api\.gitlab\.com',
        r'gitlab.*api',
        r'gitlab.*issue',
    ],
    'rss': [
        r'rss',
        r'feed',
        r'\.xml',
        r'atom',
    ],
    'music': [
        r'spotify',
        r'itunes',
        r'music',
        r'now.*playing',
        r'current.*track',
        r'last\.fm',
        r'lastfm',
    ],
    'news': [
        r'news',
        r'hacker.*news',
        r'reddit',
        r'rss.*news',
        r'feed.*news',
    ],
    'time': [
        r'date',
        r'time',
        r'clock',
        r'timer',
        r'countdown',
    ],
    'docker': [
        r'docker',
        r'container',
    ],
    'kubernetes': [
        r'kubernetes',
        r'k8s',
    ],
    'ip': [
        r'ip.*address',
        r'ipify',
        r'ip-api',
        r'whatismyip',
    ],
    'location': [
        r'location',
        r'gps',
        r'latitude',
        r'longitude',
        r'geolocation',
    ],
    'quote': [
        r'quote',
        r'brainyquote',
        r'inspirational',
    ],
    'todo': [
        r'todo',
        r'todoist',
        r'task',
    ],
    'transit': [
        r'transit',
        r'bus',
        r'train',
        r'metro',
        r'mbta',
        r'bart',
    ],
    'covid': [
        r'covid',
        r'coronavirus',
        r'pandemic',
    ],
    'nasa': [
        r'nasa',
        r'apod',
        r'astronaut',
    ],
    'none': [],  # For widgets with no external data source
}

def analyze_widget_file(file_path):
    """Analyze a widget file (JSX or CoffeeScript) to identify data sources."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
    except Exception as e:
        return {'error': str(e)}
    
    detected_sources = []
    
    # Check each data source category
    for source_type, patterns in DATA_SOURCE_PATTERNS.items():
        if source_type == 'none':
            continue
            
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                detected_sources.append(source_type)
                break  # Only need one match per category
    
    # Special case: if no sources detected and content is very simple, mark as 'none'
    if not detected_sources:
        # Check if it's just static content (no fetch, no exec, no API calls)
        has_dynamic = any([
            'fetch(' in content,
            'exec(' in content,
            'run(' in content,
            'http' in content,
            'api' in content,
            'url' in content,
        ])
        if not has_dynamic:
            detected_sources.append('none')
    
    return {
        'sources': detected_sources if detected_sources else ['unknown'],
        'file': file_path
    }

def get_widget_id_from_path(file_path):
    """Extract widget ID from file path."""
    # Path format: downloads/{widget_folder}/.../file.jsx or file.coffee
    parts = Path(file_path).parts
    if len(parts) >= 2:
        widget_folder = parts[1]
        # Remove .widget suffix if present
        widget_id = widget_folder.replace('.widget', '')
        return widget_id
    return 'unknown'

def main():
    downloads_dir = 'downloads'
    
    if not os.path.exists(downloads_dir):
        print(f"Error: {downloads_dir} directory not found")
        return
    
    # Find all widget files (JSX and CoffeeScript)
    jsx_files = glob.glob(os.path.join(downloads_dir, '**/*.jsx'), recursive=True)
    coffee_files = glob.glob(os.path.join(downloads_dir, '**/*.coffee'), recursive=True)
    all_files = jsx_files + coffee_files
    
    print(f"Found {len(jsx_files)} JSX files")
    print(f"Found {len(coffee_files)} CoffeeScript files")
    print(f"Total: {len(all_files)} widget files")
    
    # Analyze each widget
    widget_sources = defaultdict(lambda: {'sources': set(), 'files': [], 'jsx_count': 0, 'coffee_count': 0})
    
    for widget_file in all_files:
        widget_id = get_widget_id_from_path(widget_file)
        result = analyze_widget_file(widget_file)
        
        if 'error' in result:
            print(f"Error analyzing {widget_file}: {result['error']}")
            continue
        
        sources = result.get('sources', ['unknown'])
        widget_sources[widget_id]['sources'].update(sources)
        widget_sources[widget_id]['files'].append(widget_file)
        
        # Track file type counts
        if widget_file.endswith('.jsx'):
            widget_sources[widget_id]['jsx_count'] += 1
        elif widget_file.endswith('.coffee'):
            widget_sources[widget_id]['coffee_count'] += 1
    
    # Convert sets to sorted lists for JSON serialization
    results = {}
    for widget_id, data in widget_sources.items():
        results[widget_id] = {
            'sources': sorted(list(data['sources'])),
            'file_count': len(data['files']),
            'jsx_count': data['jsx_count'],
            'coffee_count': data['coffee_count']
        }
    
    # Print summary by data source type
    print("\n" + "="*80)
    print("DATA SOURCE SUMMARY")
    print("="*80)
    
    source_counts = defaultdict(int)
    for widget_id, data in results.items():
        for source in data['sources']:
            source_counts[source] += 1
    
    print("\nWidgets by data source type:")
    for source_type, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"  {source_type:20s}: {count:4d} widgets")
    
    # Print widgets with multiple sources
    print("\n" + "="*80)
    print("WIDGETS WITH MULTIPLE DATA SOURCES")
    print("="*80)
    multi_source = {k: v for k, v in results.items() if len(v['sources']) > 1}
    for widget_id, data in sorted(multi_source.items()):
        print(f"  {widget_id:40s}: {', '.join(data['sources'])}")
    
    # Save detailed results to JSON
    output_file = 'widget_data_sources.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nDetailed results saved to: {output_file}")
    
    # Print sample widgets for each category
    print("\n" + "="*80)
    print("SAMPLE WIDGETS BY CATEGORY")
    print("="*80)
    
    category_examples = defaultdict(list)
    for widget_id, data in results.items():
        for source in data['sources']:
            if len(category_examples[source]) < 5:
                category_examples[source].append(widget_id)
    
    for source_type in sorted(category_examples.keys()):
        examples = category_examples[source_type]
        print(f"\n{source_type.upper()}:")
        for widget_id in examples:
            print(f"  - {widget_id}")

if __name__ == '__main__':
    main()

