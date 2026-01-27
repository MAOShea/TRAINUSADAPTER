#!/usr/bin/env python3
"""
Extract actual URLs and API endpoints from widget files, grouped by data source category.
"""

import os
import glob
import re
import json
from collections import defaultdict
from urllib.parse import urlparse

# URL patterns to identify
URL_PATTERNS = {
    'weather': [
        r'https?://[^\s"\']*weather[^\s"\']*',
        r'https?://[^\s"\']*wttr[^\s"\']*',
        r'https?://[^\s"\']*darksky[^\s"\']*',
        r'https?://[^\s"\']*openweathermap[^\s"\']*',
        r'https?://[^\s"\']*wunderground[^\s"\']*',
        r'https?://[^\s"\']*forecast[^\s"\']*',
    ],
    'crypto': [
        r'https?://[^\s"\']*bitcoin[^\s"\']*',
        r'https?://[^\s"\']*crypto[^\s"\']*',
        r'https?://[^\s"\']*coinbase[^\s"\']*',
        r'https?://[^\s"\']*binance[^\s"\']*',
        r'https?://[^\s"\']*coinmarketcap[^\s"\']*',
        r'https?://[^\s"\']*cryptocurrency[^\s"\']*',
        r'https?://[^\s"\']*api\.cryptowat\.ch[^\s"\']*',
    ],
    'stock': [
        r'https?://[^\s"\']*yahoo.*finance[^\s"\']*',
        r'https?://[^\s"\']*alphavantage[^\s"\']*',
        r'https?://[^\s"\']*iextrading[^\s"\']*',
        r'https?://[^\s"\']*stock[^\s"\']*',
        r'https?://[^\s"\']*nasdaq[^\s"\']*',
    ],
    'github': [
        r'https?://[^\s"\']*api\.github\.com[^\s"\']*',
        r'https?://[^\s"\']*github\.com.*api[^\s"\']*',
    ],
    'gitlab': [
        r'https?://[^\s"\']*api\.gitlab\.com[^\s"\']*',
        r'https?://[^\s"\']*gitlab\.com.*api[^\s"\']*',
    ],
    'rss': [
        r'https?://[^\s"\']*\.xml[^\s"\']*',
        r'https?://[^\s"\']*rss[^\s"\']*',
        r'https?://[^\s"\']*feed[^\s"\']*',
        r'https?://[^\s"\']*atom[^\s"\']*',
    ],
    'news': [
        r'https?://[^\s"\']*hacker.*news[^\s"\']*',
        r'https?://[^\s"\']*reddit[^\s"\']*',
        r'https?://[^\s"\']*news[^\s"\']*',
    ],
    'nasa': [
        r'https?://[^\s"\']*nasa[^\s"\']*',
        r'https?://[^\s"\']*apod[^\s"\']*',
    ],
    'ip': [
        r'https?://[^\s"\']*ipify[^\s"\']*',
        r'https?://[^\s"\']*ip-api[^\s"\']*',
        r'https?://[^\s"\']*whatismyip[^\s"\']*',
    ],
    'music': [
        r'https?://[^\s"\']*spotify[^\s"\']*',
        r'https?://[^\s"\']*last\.fm[^\s"\']*',
        r'https?://[^\s"\']*lastfm[^\s"\']*',
    ],
    'quote': [
        r'https?://[^\s"\']*brainyquote[^\s"\']*',
        r'https?://[^\s"\']*quote[^\s"\']*',
    ],
    'transit': [
        r'https?://[^\s"\']*mbta[^\s"\']*',
        r'https?://[^\s"\']*bart[^\s"\']*',
        r'https?://[^\s"\']*transit[^\s"\']*',
    ],
    'covid': [
        r'https?://[^\s"\']*covid[^\s"\']*',
        r'https?://[^\s"\']*coronavirus[^\s"\']*',
    ],
}

def extract_urls_from_file(file_path):
    """Extract URLs from a widget file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return []
    
    urls = set()
    
    # Find all HTTP/HTTPS URLs
    url_pattern = r'https?://[^\s"\'<>{}|\\^`\[\]]+'
    found_urls = re.findall(url_pattern, content)
    
    for url in found_urls:
        # Clean up URL (remove trailing punctuation that might not be part of URL)
        url = url.rstrip('.,;:!?)')
        # Remove trailing slashes for consistency
        url = url.rstrip('/')
        if url:
            urls.add(url)
    
    return list(urls)

def categorize_url(url):
    """Categorize a URL by data source type."""
    url_lower = url.lower()
    
    for category, patterns in URL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                return category
    
    # Check for common patterns
    if 'api.' in url_lower:
        return 'api'
    if 'json' in url_lower:
        return 'json'
    
    return 'other'

def normalize_url(url):
    """Normalize URL to base domain/path for grouping."""
    try:
        parsed = urlparse(url)
        # Return scheme + netloc + path (without query/fragment)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
        return normalized
    except:
        return url

def main():
    downloads_dir = 'downloads'
    
    if not os.path.exists(downloads_dir):
        print(f"Error: {downloads_dir} directory not found")
        return
    
    # Find all widget files
    jsx_files = glob.glob(os.path.join(downloads_dir, '**/*.jsx'), recursive=True)
    coffee_files = glob.glob(os.path.join(downloads_dir, '**/*.coffee'), recursive=True)
    all_files = jsx_files + coffee_files
    
    print(f"Scanning {len(all_files)} widget files for URLs...")
    
    # Extract URLs from all files
    all_urls = set()
    url_to_category = {}
    url_to_widgets = defaultdict(set)
    
    for widget_file in all_files:
        # Get widget ID
        parts = widget_file.split(os.sep)
        if len(parts) >= 2:
            widget_id = parts[1].replace('.widget', '')
        else:
            widget_id = 'unknown'
        
        urls = extract_urls_from_file(widget_file)
        
        for url in urls:
            all_urls.add(url)
            url_to_widgets[url].add(widget_id)
            
            # Categorize URL
            category = categorize_url(url)
            url_to_category[url] = category
    
    # Group URLs by category
    urls_by_category = defaultdict(lambda: {'urls': set(), 'widgets': set()})
    
    for url in all_urls:
        category = url_to_category.get(url, 'other')
        normalized = normalize_url(url)
        urls_by_category[category]['urls'].add(normalized)
        urls_by_category[category]['widgets'].update(url_to_widgets[url])
    
    # Convert to sorted lists
    result = {}
    for category, data in urls_by_category.items():
        result[category] = {
            'urls': sorted(list(data['urls'])),
            'widget_count': len(data['widgets'])
        }
    
    # Save to JSON
    output_file = 'widget_data_source_urls.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nFound URLs in {len(all_urls)} unique URLs")
    print(f"Grouped into {len(result)} categories")
    print(f"Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("URLS BY CATEGORY")
    print("="*80)
    
    for category in sorted(result.keys()):
        urls = result[category]['urls']
        widget_count = result[category]['widget_count']
        print(f"\n{category.upper()} ({len(urls)} URLs, {widget_count} widgets):")
        for url in urls[:20]:  # Show first 20
            print(f"  - {url}")
        if len(urls) > 20:
            print(f"  ... and {len(urls) - 20} more")

if __name__ == '__main__':
    main()

