# TRAINUSADAPTER

A Python toolkit for downloading, analyzing, and categorizing Übersicht widgets with CoffeeScript detection.

## Overview

This project provides tools to:
- Download widget archives from a JSON manifest
- Extract and analyze widget contents
- Detect CoffeeScript usage in widgets
- Generate comprehensive CSV reports with categorization

## Features

- **Batch Download**: Download multiple widgets with filtering options
- **CoffeeScript Detection**: Recursively scan for `.coffee` files
- **Category Mapping**: Map widgets to categories and subcategories
- **Status Tracking**: Track download success/failure for each widget
- **CSV Reporting**: Generate detailed reports with all widget metadata

## Files

- `downloadfullarchive.py` - Downloads and extracts widget archives
- `generate_widget_report.py` - Generates CSV reports with analysis
- `widget_list.json` - Widget manifest with download URLs
- `widget_categories_complete.csv` - Category mappings for widgets

## Usage

### Download all widgets
```bash
python3 downloadfullarchive.py
```

### Download specific widgets
```bash
python3 downloadfullarchive.py --widgets "AnalogClock,BackgroundGrid,WeatherTV"
```

### Download from file
```bash
python3 downloadfullarchive.py --widget-file missing_widgets.txt
```

### Generate report
```bash
python3 generate_widget_report.py
```

## Requirements

- Python 3.6+
- requests
- zipfile (built-in)
- csv (built-in)
- json (built-in)
- glob (built-in)
- argparse (built-in)

## Results

The final CSV report includes:
- Widget metadata (ID, name, author, description)
- Download URLs and filenames
- Category and subcategory classifications
- CoffeeScript usage detection (Y/N/Download Failed/Not Attempted)

## Statistics

Based on analysis of 434 widgets:
- **91.5%** successfully downloaded
- **76.3%** of successful downloads use CoffeeScript
- **8.5%** had broken download URLs
