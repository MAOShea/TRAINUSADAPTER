#!/usr/bin/env python3
"""
Analyze widget files to assess training data strategy.
Determines which widgets are too large for max_sequence_length and recommends chunking/exclusion strategies.
"""

import os
import json
import csv
import glob
from pathlib import Path
from collections import defaultdict

# Rough token estimation: ~4 chars per token for code (conservative)
CHARS_PER_TOKEN = 4
DEFAULT_MAX_SEQUENCE_LENGTH = 4095

def estimate_tokens(text_length, chars_per_token=CHARS_PER_TOKEN):
    """Estimate token count from character length"""
    return int(text_length / chars_per_token)

def analyze_widget_files(csv_file_path, downloads_dir='downloads'):
    """
    Analyze widget JSX files to determine sizes and provide chunking recommendations.
    
    Args:
        csv_file_path: Path to widget_processing_results.csv
        downloads_dir: Directory containing widget files
    """
    
    # Load CSV to get widget info
    widgets = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('PS_isJSX') == 'Y':
                widgets.append({
                    'id': row['OS_widget_id'],
                    'folder': row['PS_widgetfoldername']
                })
    
    print(f"Analyzing {len(widgets)} JSX widgets...\n")
    
    # Analyze each widget
    results = []
    for widget in widgets:
        widget_path = os.path.join(downloads_dir, widget['folder'])
        
        if not os.path.exists(widget_path):
            continue
        
        # Find all JSX files
        jsx_files = glob.glob(os.path.join(widget_path, '**/*.jsx'), recursive=True)
        
        total_chars = 0
        total_lines = 0
        file_sizes = []
        
        for jsx_file in sorted(jsx_files):
            try:
                with open(jsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    chars = len(content)
                    lines = content.count('\n')
                    total_chars += chars
                    total_lines += lines
                    file_sizes.append({
                        'file': os.path.relpath(jsx_file, widget_path),
                        'chars': chars,
                        'lines': lines
                    })
            except Exception as e:
                print(f"Warning: Could not read {jsx_file}: {e}")
        
        estimated_tokens = estimate_tokens(total_chars)
        
        results.append({
            'widget_id': widget['id'],
            'widget_folder': widget['folder'],
            'total_chars': total_chars,
            'total_lines': total_lines,
            'estimated_tokens': estimated_tokens,
            'num_files': len(jsx_files),
            'file_sizes': file_sizes,
            'exceeds_limit': estimated_tokens > DEFAULT_MAX_SEQUENCE_LENGTH
        })
    
    return results

def print_analysis(results, max_sequence_length=DEFAULT_MAX_SEQUENCE_LENGTH):
    """Print detailed analysis and recommendations"""
    
    # Sort by token count
    results.sort(key=lambda x: x['estimated_tokens'], reverse=True)
    
    total_widgets = len(results)
    exceeding_limit = sum(1 for r in results if r['exceeds_limit'])
    within_limit = total_widgets - exceeding_limit
    
    print("=" * 80)
    print("WIDGET SIZE ANALYSIS")
    print("=" * 80)
    print(f"\nTotal widgets analyzed: {total_widgets}")
    print(f"Max sequence length limit: {max_sequence_length} tokens")
    print(f"\nWidgets exceeding limit: {exceeding_limit} ({exceeding_limit/total_widgets*100:.1f}%)")
    print(f"Widgets within limit: {within_limit} ({within_limit/total_widgets*100:.1f}%)")
    
    # Statistics
    token_counts = [r['estimated_tokens'] for r in results]
    if token_counts:
        print(f"\nToken Statistics:")
        print(f"  Min: {min(token_counts)} tokens")
        print(f"  Max: {max(token_counts)} tokens")
        print(f"  Average: {sum(token_counts)/len(token_counts):.0f} tokens")
        print(f"  Median: {sorted(token_counts)[len(token_counts)//2]} tokens")
    
    # Show top 10 largest widgets
    print(f"\n{'='*80}")
    print("TOP 10 LARGEST WIDGETS (by estimated tokens)")
    print("=" * 80)
    print(f"{'Widget ID':<30} {'Tokens':<12} {'Chars':<12} {'Files':<8} {'Status'}")
    print("-" * 80)
    
    for r in results[:10]:
        status = "⚠️ EXCEEDS" if r['exceeds_limit'] else "✓ OK"
        print(f"{r['widget_id']:<30} {r['estimated_tokens']:<12} {r['total_chars']:<12} {r['num_files']:<8} {status}")
    
    # Show widgets exceeding limit
    if exceeding_limit > 0:
        print(f"\n{'='*80}")
        print(f"WIDGETS EXCEEDING {max_sequence_length} TOKEN LIMIT")
        print("=" * 80)
        print(f"{'Widget ID':<30} {'Tokens':<12} {'Chars':<12} {'Files':<8}")
        print("-" * 80)
        
        for r in results:
            if r['exceeds_limit']:
                print(f"{r['widget_id']:<30} {r['estimated_tokens']:<12} {r['total_chars']:<12} {r['num_files']:<8}")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if exceeding_limit == 0:
        print("\n✓ All widgets fit within the limit. No chunking needed!")
    else:
        print(f"\n⚠️ {exceeding_limit} widgets exceed the limit. Consider these strategies:\n")
        
        print("1. EXCLUSION STRATEGY:")
        print(f"   - Remove {exceeding_limit} large widgets from training")
        print(f"   - Dataset size: {within_limit} widgets")
        print(f"   - Pros: Simple, ensures all data fits")
        print(f"   - Cons: Loses {exceeding_limit/total_widgets*100:.1f}% of training data\n")
        
        print("2. TRUNCATION STRATEGY:")
        print(f"   - Keep all widgets, truncate to {max_sequence_length} tokens")
        print(f"   - Dataset size: {total_widgets} widgets")
        print(f"   - Pros: Keeps all widgets")
        print(f"   - Cons: Large widgets lose tail content (data loss)\n")
        
        print("3. HYBRID STRATEGY:")
        print(f"   - Exclude extremely large widgets (>2x limit)")
        print(f"   - Truncate moderately large widgets")
        double_limit = max_sequence_length * 2
        extreme_count = sum(1 for r in results if r['estimated_tokens'] > double_limit)
        if extreme_count > 0:
            print(f"   - Exclude {extreme_count} extreme widgets")
            print(f"   - Truncate {exceeding_limit - extreme_count} moderate widgets")
        print(f"   - Dataset size: ~{total_widgets - extreme_count} widgets")
        print(f"   - Pros: Balance between data retention and quality")
        print(f"   - Cons: More complex implementation\n")
        
        print("4. CHUNKING STRATEGY:")
        print(f"   - Split large widgets into multiple training examples")
        print(f"   - Each chunk must include required exports (command, refreshFrequency, render, className)")
        print(f"   - Pros: Preserves all widget content")
        print(f"   - Cons: Complex, may require manual chunking logic\n")
    
    # Export detailed results
    output_file = 'widget_size_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'max_sequence_length': max_sequence_length,
            'total_widgets': total_widgets,
            'exceeding_limit': exceeding_limit,
            'within_limit': within_limit,
            'widgets': results
        }, f, indent=2)
    
    print(f"\n✓ Detailed results saved to: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze widget sizes for training data strategy')
    parser.add_argument('--csv', default='widget_processing_results.csv', 
                       help='Path to widget_processing_results.csv')
    parser.add_argument('--downloads', default='downloads', 
                       help='Directory containing widget files')
    parser.add_argument('--max-tokens', type=int, default=DEFAULT_MAX_SEQUENCE_LENGTH,
                       help='Maximum sequence length in tokens (default: 4095)')
    
    args = parser.parse_args()
    
    results = analyze_widget_files(args.csv, args.downloads)
    print_analysis(results, args.max_tokens)

if __name__ == '__main__':
    main()

