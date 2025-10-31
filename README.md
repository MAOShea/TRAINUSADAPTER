# TRAINUSADAPTER

A Python toolkit for downloading, analyzing, and categorizing Übersicht widgets with CoffeeScript detection.

## Overview

This project provides tools to:
- Download widget archives from a JSON manifest
- Extract and analyze widget contents
- Detect CoffeeScript usage in widgets
- Generate comprehensive CSV reports with categorization
- Create AI prompts for JSX widgets
- Perform AI-assisted curation and categorization
- Generate JSONL training datasets for Apple adapter model fine-tuning

**Training Format Decision:** This project uses a **one-shot (single-turn) conversation format** for adapter training. Each training example consists of a user request followed by a complete widget response (`[system, user, assistant]`). While multi-turn incremental improvements (e.g., "create widget" → "align it right" → "make font bold") are recognized as a potential use case, they are not currently implemented. See section 6.1.1 for detailed discussion.

## Important Notes

**Temporary Files:** All temporary files created during processing (analysis files, intermediate data, etc.) must be created in the `temp/` folder to keep the workspace clean and organized.

## Complete Process Overview

The full workflow for processing Übersicht widgets follows these steps:

### 0. Prerequisites: Widget Manifest
Before starting, you need a `widget_list.json` file containing the widget manifest with download URLs. This file should contain an array of widget objects with properties like:
- `id` - Unique widget identifier
- `name` - Widget display name  
- `author` - Widget creator
- `description` - Widget description
- `download_url` - Direct download URL to the widget archive

**How to obtain:** Download `widget_list.json` from the [Übersicht GitHub repository](https://github.com/felixhageloh/uebersicht).

**Note:** The `widget_list.json` file is the source data for the entire pipeline. All subsequent steps depend on this manifest.

### 1. Download Widgets
```bash
/usr/bin/python3 /Users/mike/Documents/TrainUSAdapter/downloadfullarchive.py 2>&1 | tee download_log.txt
```
Downloads all widget archives from the JSON manifest and extracts them to the `downloads/` directory.

### 2. Generate Analysis Report
```bash
python3 generate_widget_report.py
```
Analyzes downloaded widgets to determine:
- CoffeeScript usage (`PS_iscoffee`)
- CoffeeScript complexity (`PS_complexcoffee`) 
- JSX usage (`PS_isJSX`)
- Widget folder names (`PS_widgetfoldername`)

### 3. Generate AI Prompts
For each JSX widget (`PS_isJSX = "Y"`):
1. Verify widget folder exists at `downloads/[PS_widgetfoldername]`
2. Find and analyze ALL JSX files in that folder
3. Analyze JSX code structure, functionality, and styling approach
4. Combine insights from all JSX files with `OS_description`
5. Generate comprehensive prompt: "Create an Übersicht widget that [OS_description]. The widget should [key functionality from JSX analysis] using React/JSX with [styling approach]."
6. Save prompt to `prompts/{widget_id}.prompt`

**Missing Prompt Files (14 widgets):**
The following JSX widgets need prompt generation:
1. `CryptoMarketCap`
2. `Docker-Box-Widget` 
3. `FastFetch`
4. `RedditMembers.widget`
5. `TautulliWidget`
6. `battery-bar`
7. `march-covid`
8. `ubersicht-docker-widget`
9. `ubersicht-quote-of-the-day`
10. `ubersicht-time-remaining`
11. `uebersicht-currenttrack-widget`
12. `uebersicht-fetch`
13. `uebersicht-ip`
14. `vintage-apple.widget`

## RESUME WORK: Generate Missing Prompt Files

**Current Status:** 61 out of 75 JSX widgets have prompt files. 14 widgets are missing prompts.

**Task:** Generate AI prompts for the 14 missing JSX widgets listed above.

**Instructions:**
1. For each of the 14 missing widgets:
   - Find the widget folder at `downloads/[PS_widgetfoldername]` (check CSV for exact path)
   - Locate and analyze ALL JSX files in that folder
   - Read the widget's `OS_description` from the CSV
   - Generate a comprehensive prompt: "Create an Übersicht widget that [OS_description]. The widget should [key functionality from JSX analysis] using React/JSX with [styling approach]."
   - Save the prompt to `prompts/{widget_id}.prompt`

2. **Process all 14 widgets** to complete the dataset for training.

3. **Verify completion** by running: `python3 create_dataset.py --csv widget_processing_results.csv --set test_complete`

**Expected Result:** All 75 JSX widgets should have prompt files, and the dataset creation should process all widgets without skipping any.

### 4. AI-Assisted Curation
Generate widget categories and inject them into the CSV:

#### 4a. Generate Categories
Use the AI prompt in the "AI Prompt for Category Generation" section below to create `widget_categorisation.json`.

#### 4b. Inject Categories
```bash
python3 inject_categories.py
```
This updates the CSV with `AI_category` and `AI_secondary_category` columns based on the JSON file.

### 5. Generate Dataset
```bash
python3 generate_json_dataset.py
```
Convert the processed CSV into a structured dataset for training.

### 6. Create JSONL Training Dataset
```bash
python3 create_dataset.py --csv widget_processing_results.csv --set my_dataset_v1
```
Generate JSONL files for Apple adapter model training from CSV and widget code files.

**Parameters:**
- `--csv`: Path to the widget_processing_results.csv file
- `--set`: Dataset name (creates folder under `/datasets`)

**Output Structure:**
```
/datasets/{set_name}/
├── train.jsonl
├── valid.jsonl
└── test.jsonl
```

**Features:**
- Filters for JSX widgets only (`PS_isJSX = "Y"`)
- Concatenates all JSX files in each widget folder
- Adds filename comments for context
- 80/10/10 train/validation/test split with random shuffling
- Chat format suitable for Apple's adapter training
- Handles missing files gracefully with warnings

**Data Format:**
Each JSONL line contains a chat conversation following **Apple's adapter training schema** (compatible with OpenAI Chat Completion format):
```json
[
  {
    "role": "system",
    "content": "SYSTEM_PROMPT (includes tool instructions)",
    "tools": [{"type": "function", "function": {...}}]
  },
  {
    "role": "user",
    "content": "Create an Übersicht widget that..."
  },
  {
    "role": "assistant",
    "content": "// index.jsx\nexport const command = ...\nexport const render = ...\n..."
  }
]
```

**Format Reference:**
- **Official Standard**: Apple's adapter training schema (see `schema.md` in adapter training toolkit)
- **Compatibility**: Compatible with OpenAI Chat Completions API format
- **Structure**: System message with tools definition, user prompt, assistant response with complete widget code

#### 6.1.1 Conversation Format: One-Shot Approach

**Current Decision:** We have elected to use a **one-shot (single-turn) conversation format** for training.

**What This Means:**
- Each training example is a single request → complete widget response
- Structure: `[system, user, assistant]` (3 messages per example)
- The user asks once, and the assistant responds with the complete widget JSX code
- This matches real-world usage where users typically request a complete widget in one interaction

**Training Example:**
```json
[
  {"role": "system", "content": "...", "tools": [...]},
  {"role": "user", "content": "Create a widget with a button labeled 'Hello World'"},
  {"role": "assistant", "content": "export const command = ...\nexport const render = ...\n// complete widget code"}
]
```

**Future Consideration: Multi-Turn Incremental Improvements**
While not currently implemented, we recognize a potential use case for **multi-turn conversations** where users incrementally improve widgets:
- Turn 1: "Create a widget with a button"
- Turn 2: "Align it to the right edge"
- Turn 3: "Make the font bold"

**Why We're Not Doing Multi-Turn Yet:**
1. **Training Data Complexity**: Generating realistic incremental improvement sequences requires either manual curation or sophisticated synthetic generation
2. **Current Focus**: One-shot generation matches the primary use case and is simpler to implement
3. **Data Quality**: We want high-quality training examples; multi-turn requires ensuring each incremental step is realistic and coherent

**Multi-Turn Implementation (Future Work):**
If multi-turn incremental improvements are desired, the implementation would require:
- New data structure: `multiturn_conversations/{widget_id}.json` with conversation sequences
- Modified `create_dataset.py` to support both single-turn and multi-turn examples
- Strategy for generating/curating incremental improvement sequences
- Mixed datasets: supporting both formats in the same training set

For now, the adapter is trained on single-turn conversations where the assistant generates complete widgets in one response.

#### 6.1 Design: Tool Call Integration

The `create_dataset.py` script implements a sophisticated approach to training adapter models for **tool calling** rather than just code generation. This design enables the adapter to learn when and how to call the `WriteUbersichtWidgetToFileSystem` tool.

**Core Design Philosophy:**
- **Tool-First Approach**: Instead of generating JSX code directly, the adapter learns to call tools with extracted parameters
- **Parameter Extraction**: Four extraction functions parse existing JSX code to extract tool parameters
- **Realistic Training Data**: Uses actual widget code to create realistic tool calls with proper parameter values

**Extraction Functions:**

1. **`extract_bash_command(code)`**
   - **Purpose**: Extracts the bash command that Übersicht will execute
   - **Pattern**: `export const command = \`([^`]+)\``
   - **Returns**: The bash command string (e.g., `"ps aux | grep python"`)
   - **Why**: The bash command determines what data the widget displays

2. **`extract_refresh_frequency(code)`**
   - **Purpose**: Extracts how often the widget refreshes its data
   - **Pattern**: `export const refreshFrequency = (\d+)`
   - **Returns**: Refresh rate in milliseconds (defaults to 1000 if not found)
   - **Why**: Controls widget update frequency and system resource usage

3. **`extract_render_function(code)`**
   - **Purpose**: Extracts the React component that renders the widget
   - **Pattern**: `export const render = ({[^}]+}) =>`
   - **Returns**: Complete React functional component as string
   - **Why**: This is the core rendering logic that displays the bash command output

4. **`extract_css_positioning(code)`**
   - **Purpose**: Extracts CSS positioning for absolute placement
   - **Pattern**: `export const className = \`([^`]+)\``
   - **Returns**: CSS positioning string (e.g., `"top: 20px; left: 20px;"`)
   - **Why**: Determines where the widget appears on the desktop

**Training Data Structure:**
Each training example follows this pattern:
```json
[
  {
    "role": "system",
    "content": "You are an Übersicht widget designer... [tool instructions]",
    "tools": [{"type": "function", "function": {...}}]
  },
  {
    "role": "user", 
    "content": "Create an Übersicht widget that..."
  },
  {
    "role": "assistant",
    "content": "I'll create that widget for you.",
    "tool_calls": [{
      "id": "call_widget_id",
      "type": "function",
      "function": {
        "name": "WriteUbersichtWidgetToFileSystem",
        "arguments": {
          "bashCommand": "ps aux | grep python",
          "refreshFrequency": 1000,
          "renderFunction": "({output}) => { return <div className='widget'>{output}</div> }",
          "cssPositioning": "top: 20px; left: 20px;"
        }
      }
    }]
  }
]
```

**Key Benefits:**
- **Realistic Tool Calls**: Uses actual widget parameters instead of synthetic data
- **Parameter Accuracy**: Extraction functions ensure tool calls have correct parameter types and values
- **Tool Learning**: Adapter learns the relationship between user requests and tool parameter extraction
- **Code Quality**: Maintains high-quality JSX generation while adding tool calling capability

## Detailed JSX Processing Instructions

Process the CSV file `widget_processing_results.csv` (which has a header row and 435 data rows):

For each data row where `PS_iscoffee = "N"`:
1. Verify the widget folder exists at `downloads/[PS_widgetfoldername]`
2. Find and analyze ALL JSX files in that folder (no prioritization, analyze everything)
3. Analyze the JSX code structure, functionality, and styling approach from all files
4. Combine insights from all JSX files with `OS_description` to create a comprehensive prompt
5. Generate a prompt like: "Create an Übersicht widget that [OS_description]. The widget should [key functionality from all JSX analysis] using React/JSX with [styling approach from all files]."
6. Write the prompt to the `AI_prompt` column
7. Update the CSV file with the new `AI_prompt` values and save it to disk

## Features

- **Batch Download**: Download multiple widgets with filtering options
- **CoffeeScript Detection**: Recursively scan for `.coffee` files
- **Category Mapping**: Map widgets to categories and subcategories
- **Status Tracking**: Track download success/failure for each widget
- **CSV Reporting**: Generate detailed reports with all widget metadata

## Files

### Core Scripts
- `downloadfullarchive.py` - Downloads and extracts widget archives from `widget_list.json`
- `generate_widget_report.py` - Generates CSV reports with analysis
- `inject_categories.py` - Injects AI categories into CSV from JSON file
- `create_dataset.py` - Creates JSONL training datasets from CSV and widget code files

### Data Files
- `widget_list.json` - **REQUIRED**: Widget manifest with download URLs (source data for entire pipeline)
- `widget_categorisation.json` - AI-generated widget categories (created by analysis)
- `widget_processing_results.csv` - Generated CSV report with all widget metadata and analysis results

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

### Inject AI categories
```bash
python3 inject_categories.py
```

**Note:** This requires `widget_categorisation.json` to exist with widget categorizations.

## Widget Categorization System

The categorization system uses `widget_categorisation.json` to classify widgets and inject categories into the CSV file.

### How It Works

1. **Generate categories**: Use the AI prompt below to create `widget_categorisation.json`
2. **Inject categories**: Run `python3 inject_categories.py` to update the CSV
3. **Verify results**: Check the updated CSV file

### JSON File Structure

The `widget_categorisation.json` file uses this format:
```json
{
  "categories": {
    "1": "Time & Date",
    "2": "System Monitoring", 
    "3": "Weather",
    "4": "Music & Media"
  },
  "widgets": {
    "AnalogClock": [1, 17],
    "CPU-Usage-bar-Widget": [2, 16],
    "WeatherTV": [3, 16]
  }
}
```

Where:
- `categories`: Maps numeric IDs to category names
- `widgets`: Maps widget IDs to `[primary_category_id, secondary_category_id]` arrays

### Script Output

The `inject_categories.py` script will:
- Update the CSV file in-place with `AI_category` and `AI_secondary_category` columns
- Report how many widgets were updated
- Show any widgets not found in the categorizations
- Preserve all existing data while updating only the AI category columns

## AI Prompt for Category Generation

**Use this prompt with an AI assistant to generate `widget_categorisation.json`:**

```
Please perform the following steps:

1. **Read the CSV file** `widget_processing_results.csv` and analyze the `OS_description` column for each widget.

2. **Infer categories**: For each widget, analyze its description to determine:
   - A primary category (main function/purpose)
   - A secondary category (additional characteristic or sub-function)

3. **Collect all unique categories**: 
   - Gather all primary and secondary categories from all widgets
   - Create a unique list of all distinct categories
   - Assign sequential numeric IDs starting from 1

4. **Generate the JSON file** `widget_categorisation.json` with this structure:
   ```json
   {
     "categories": {
       "1": "System Monitoring",
       "2": "Real-time Data",
       "3": "Visual Display",
       ...
     },
     "widgets": {
       "widget_id_1": [1, 2],
       "widget_id_2": [2, 3],
       ...
     }
   }
   ```

5. **Process all widgets** in the CSV file (no filtering needed).

6. **Output format**:
   - `categories`: Object with numeric keys (strings) and category names as values
   - `widgets`: Object with widget IDs as keys and arrays of two category IDs as values

The goal is to create a comprehensive categorization system where each widget has both a primary and secondary category, and all unique categories are numbered sequentially.
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

## CSV Column Structure

The generated `widget_processing_results.csv` contains 14 columns organized by prefix:

### OS_ (Original Source) Columns
Data sourced directly from `widget_list.json`:
- **`OS_widget_id`** - Unique widget identifier
- **`OS_name`** - Widget display name
- **`OS_author`** - Widget creator/author
- **`OS_description`** - Widget description
- **`OS_download_url`** - Direct download URL

### PS_ (Processing Status) Columns
Generated during processing and analysis:
- **`PS_filename`** - ZIP filename (extracted from download URL)
- **`PS_iscoffee`** - CoffeeScript detection result (Y/N/Download Failed/Not Attempted/Extraction Failed)
- **`PS_complexcoffee`** - CoffeeScript complexity analysis (True/False, only when PS_iscoffee=Y)
- **`PS_isJSX`** - JSX detection result (Y/N/Download Failed/Not Attempted/Extraction Failed)
- **`PS_widgetfoldername`** - Relative path to widget folder in downloads/ directory

**Note:** `PS_iscoffee` and `PS_isJSX` are independent flags. A widget can have both CoffeeScript and JSX files (e.g., during migration from CoffeeScript to React).

### AI_ (AI Analysis) Columns
Data generated by AI (Claude) during curation:
- **`AI_category`** - Primary category classification
- **`AI_secondary_category`** - Secondary category classification
- **`AI_prompt`** - AI-generated prompt based on description and code

### CT_ (Curation Task) Columns
Decisions made during the curation step:
- **`CT_set`** - Dataset assignment (training/validation/test or tr/v/te). Empty = excluded
- **`CT_comment`** - Optional curator notes about the decision

### Column Prefix Legend
- **OS_**: Original Source data from widget manifest
- **PS_**: Processing Status and analysis results
- **AI_**: AI-generated or analyzed data (categories, prompts)
- **CT_**: Curation Task decisions and notes

## Current Processing Status

### AI Prompt Generation Progress
- **Total JSX widgets to process**: 73
- **Completed**: 1 (1.4%)
- **Remaining**: 72 (98.6%)
- **Status**: Starting new full run of widget processing
- **Approach**: Complete regeneration of all AI prompts for JSX widgets

### Processing Details
- Processing all JSX widgets where `PS_isJSX = "Y"`
- Generating AI prompts based on widget descriptions and functionality
- Each prompt includes technical requirements, styling approach, and positioning details

### Statistics

Based on analysis of 434 widgets:
- **91.5%** successfully downloaded
- **76.3%** of successful downloads use CoffeeScript
- **8.5%** had broken download URLs

### Recent Updates
- 🔄 Starting new full run of AI prompt generation for all 95 JSX widgets
- 📝 Regenerating comprehensive prompts covering React/JSX patterns, API integrations, styling approaches
- 🎯 Processing all JSX widgets with fresh analysis and improved prompt generation
- 📝 All prompts follow consistent format: "Create an Übersicht widget that..."

## How to Resume AI Prompt Generation

### Current Task
Process all JSX widgets in `widget_processing_results.csv` where `PS_isJSX = "Y"` and create individual prompt files.

### Method
1. Find JSX widgets: `find downloads -name "*.jsx" | grep -v [processed_list]`
2. Read JSX files to analyze code structure, functionality, styling
3. Generate prompt: "Create an Übersicht widget that [OS_description]. The widget should [functionality] using React/JSX with [styling]."
4. Create individual prompt file: `prompts/{widget_id}.prompt` containing the generated prompt

### Identifying JSX Widgets in CSV
To identify JSX widgets in `widget_processing_results.csv`, look for rows where `PS_isJSX = "Y"`:

**Correct command to count JSX widgets:**
```bash
awk -F',' '$12 == "Y" {print $1}' widget_processing_results.csv | wc -l
```

**Correct command to list JSX widget IDs:**
```bash
awk -F',' '$12 == "Y" {print $1}' widget_processing_results.csv
```

**Pattern explanation:**
- The command `awk -F',' '$12 == "Y"'` targets column 12 specifically:
  - Column 12 = `PS_isJSX` (indicates JSX files detected)
  - This avoids counting CoffeeScript widgets (column 10 = `PS_iscoffee`)

**Note:** This will find widgets with JSX files regardless of whether they also have CoffeeScript files.

### Resuming Work
To resume AI prompt generation:

1. **Find next unprocessed widget:**
   ```bash
   # Get all JSX widgets
   awk -F',' '$12 == "Y" {print $1}' widget_processing_results.csv > all_jsx_widgets.txt
   
   # Get already processed widgets (from prompts directory)
   ls prompts/ | sed 's/\.prompt$//' > processed_widgets.txt
   
   # Find next widget to process
   comm -23 all_jsx_widgets.txt processed_widgets.txt | head -1
   ```

2. **Check progress:**
   ```bash
   # Count remaining widgets
   comm -23 all_jsx_widgets.txt processed_widgets.txt | wc -l
   ```

3. **Continue from step 2** in the Method section above

### File Structure
- `prompts/` - Directory containing individual prompt files
- Each prompt file named as `{widget_id}.prompt` (e.g., `Circular-CPU.prompt`)
- Prompt files contain the full AI generation prompt for that specific widget

### Processed Widgets (exclude from search)
uebersicht-jira-filter,gitlabissues,currenttrack,UeberPlayer,CryptoMarketCap,PostNord,task-deadline,helldivers,hacker-news,oura,MiniBar,FroxceySidebar,istats,monit,os-version-uptime,quotes,github,microcalendar,time-remaining,docker-box,RedditMembers,Docker,wttr-moon,fetch,leetcode-glance,newsticker,wallpaper,TodoListWidget,trash-empty,Persona_5_Calendar,particles,wttr,position,leetcode-activity,vintage-apple,OnlineChecker,uebersicht-BinanceCryptoPrices,purpleaqi,drunk-o-clock,Really-Simple-Spotify,photo-frame,ubersicht-clock,Music-Craft,TautulliWidget,battery-bar,ubersitch-world-clock,profile,french-revolutionary,simple-white-calendar,zelda-battery,gitissues,WeatherTV,icalPal,quote-of-the-day,simple-calendar,walking_fam_pixart
