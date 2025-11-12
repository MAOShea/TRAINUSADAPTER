#!/usr/bin/env python3
"""
Diversify prompt leading phrases across all prompt files.
Replaces only the opening phrase while preserving the rest of each prompt.
"""

import os
import re
import random
from pathlib import Path

# Define variations with categories
VARIATIONS = {
    'direct': [
        "Create an Übersicht widget that",
        "Build an Übersicht widget that",
        "Make an Übersicht widget that",
        "Design an Übersicht widget that",
        "Generate an Übersicht widget that",
        "Build me an Übersicht widget that",
        "Create a widget that",
        "Build a widget that",
        "Make a widget that",
        "Design a widget that",
    ],
    'indirect': [
        "I need an Übersicht widget that",
        "I want an Übersicht widget that",
        "I'd like an Übersicht widget that",
        "I need a widget that",
        "I want a widget that",
        "I'd like a widget that",
        "I'm looking for an Übersicht widget that",
        "I'm looking for a widget that",
    ],
    'question': [
        "Can you create an Übersicht widget that",
        "Can you build an Übersicht widget that",
        "Can you make an Übersicht widget that",
        "Can you design an Übersicht widget that",
        "Could you create an Übersicht widget that",
        "Could you build an Übersicht widget that",
        "Would you create an Übersicht widget that",
        "Can you create a widget that",
        "Can you build a widget that",
        "Can you make a widget that",
    ],
    'descriptive': [
        "An Übersicht widget that",
        "A widget that",
        "Show me an Übersicht widget that",
        "Show me a widget that",
        "Display an Übersicht widget that",
        "Display a widget that",
        "Give me an Übersicht widget that",
        "Give me a widget that",
    ],
    'other': [
        "Build an Übersicht widget for",
        "Make an Übersicht widget for",
        "Create an Übersicht widget for",
        "Design an Übersicht widget for",
        "Generate a widget that",
        "Produce an Übersicht widget that",
        "Develop an Übersicht widget that",
        "Implement an Übersicht widget that",
        "I'm building an Übersicht widget that",
        "I'm making an Übersicht widget that",
        "I'm creating an Übersicht widget that",
        "I'm designing an Übersicht widget that",
        "Whip up an Übersicht widget that",
        "Put together an Übersicht widget that",
        "Come up with an Übersicht widget that",
        "Make me an Übersicht widget that",
    ]
}

# Distribution percentages (applied to 87 prompts)
# 30-40% direct: 26-35 prompts
# 20-25% indirect: 17-22 prompts  
# 15-20% question: 13-17 prompts
# 10-15% descriptive: 9-13 prompts
# 5-10% other: 4-9 prompts

def assign_variations(total_prompts=87):
    """Assign variation categories to prompts based on recommended distribution."""
    assignments = []
    
    # Calculate counts (using mid-range values)
    direct_count = 31  # ~35.6%
    indirect_count = 20  # ~23%
    question_count = 15  # ~17.2%
    descriptive_count = 11  # ~12.6%
    other_count = 10  # ~11.5% (sum to 87)
    
    # Create assignment list
    assignments.extend(['direct'] * direct_count)
    assignments.extend(['indirect'] * indirect_count)
    assignments.extend(['question'] * question_count)
    assignments.extend(['descriptive'] * descriptive_count)
    assignments.extend(['other'] * other_count)
    
    # Randomize
    random.shuffle(assignments)
    return assignments

def extract_leading_phrase(text):
    """Extract the leading phrase that needs to be replaced."""
    # Common patterns to match
    patterns = [
        r'^Create an Übersicht widget that\s+',
        r'^Create a widget that\s+',
        r'^Build an Übersicht widget that\s+',
        r'^Make an Übersicht widget that\s+',
        r'^Design an Übersicht widget that\s+',
        r'^Generate an Übersicht widget that\s+',
        # Add more patterns if needed
    ]
    
    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    # Fallback: try to find "widget that" pattern
    match = re.match(r'^[^.]*widget that\s+', text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    
    # If no pattern found, return first sentence up to "that"
    match = re.match(r'^([^.]*that)\s+', text)
    if match:
        return match.group(1).strip()
    
    return None

def replace_leading_phrase(text, new_phrase):
    """Replace the leading phrase with a new one, preserving the rest."""
    old_phrase = extract_leading_phrase(text)
    
    if old_phrase:
        # Remove the old phrase and any leading whitespace
        rest = text[len(old_phrase):].lstrip()
        
        # Handle "for" variations - they need to be converted to "that" if the rest
        # doesn't work grammatically with "for" (e.g., if rest starts with a verb)
        if new_phrase.endswith('for'):
            # Check if the rest starts with a verb (like "displays", "shows", etc.)
            # If so, convert "for" to "that" for proper grammar
            verb_pattern = r'^(displays?|shows?|fetches?|executes?|renders?|creates?|builds?|makes?)'
            if re.match(verb_pattern, rest, re.IGNORECASE):
                # Convert "for" to "that"
                new_phrase = new_phrase.replace(' for', ' that')
        
        return f"{new_phrase} {rest}"
    else:
        # If we can't find the pattern, try a simple replacement
        # Replace "Create an Übersicht widget that" at the start
        new_phrase_fixed = new_phrase
        if new_phrase.endswith('for'):
            # Check if replacement would create bad grammar
            if re.search(r'Create an Übersicht widget that\s+(displays?|shows?|fetches?)', text, re.IGNORECASE):
                new_phrase_fixed = new_phrase.replace(' for', ' that')
        
        text = re.sub(r'^Create an Übersicht widget that\s+', f'{new_phrase_fixed} ', text, flags=re.IGNORECASE)
        text = re.sub(r'^Create a widget that\s+', f'{new_phrase_fixed} ', text, flags=re.IGNORECASE)
        return text

def process_prompts(prompts_dir='prompts'):
    """Process all prompt files and diversify their leading phrases."""
    prompts_dir = Path(prompts_dir)
    if not prompts_dir.exists():
        print(f"Error: {prompts_dir} directory not found")
        return
    
    # Get all prompt files
    prompt_files = sorted(prompts_dir.glob('*.prompt'))
    total = len(prompt_files)
    
    if total == 0:
        print(f"No prompt files found in {prompts_dir}")
        return
    
    print(f"Found {total} prompt files")
    
    # Assign variations
    assignments = assign_variations(total)
    
    # Track distribution
    distribution = {'direct': 0, 'indirect': 0, 'question': 0, 'descriptive': 0, 'other': 0}
    
    # Process each file
    for i, prompt_file in enumerate(prompt_files):
        try:
            # Read the prompt
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Get assigned category and pick random variation from that category
            category = assignments[i]
            new_phrase = random.choice(VARIATIONS[category])
            distribution[category] += 1
            
            # Replace leading phrase
            new_content = replace_leading_phrase(content, new_phrase)
            
            # Write back
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(new_content + '\n')
            
            print(f"Updated {prompt_file.name}: '{new_phrase}'")
            
        except Exception as e:
            print(f"Error processing {prompt_file.name}: {e}")
    
    # Print distribution summary
    print(f"\nDistribution summary:")
    for category, count in distribution.items():
        percentage = (count / total) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")

if __name__ == '__main__':
    # Set random seed for reproducibility (optional)
    random.seed(42)
    process_prompts()

