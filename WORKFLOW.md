# Complete Training Data Pipeline Workflow

## Overview

This document describes how all Python scripts work together to create training data for adapter model fine-tuning.

## Quick Reference: Pipeline Sequence

**Complete workflow summary - stages in execution order:**

1. **Prerequisites** → Manual: Download `widget_list.json` from Übersicht GitHub repo

2. **Data Collection** → `downloadfullarchive.py` → Downloads widgets to `downloads/`

3. **Widget Analysis** → `generate_widget_report.py` → Generates `widget_processing_results.csv`

4. **Prompt Generation** → Manual/AI-assisted → Creates `prompts/{widget_id}.prompt` files

5. **Size Evaluation** (Optional) → `evaluate_training_data_size.py` → Evaluates token counts, generates strategy file for create_dataset.py
   - Optional: `analyze_widget_sizes.py` for quick widget-only check

6. **Dataset Generation** → `create_dataset.py --csv widget_processing_results.csv --set {name} --system-prompt systemPrompt_v6` → Creates `datasets/{name}/*.jsonl`

7. **Model Training** → Apple's adapter training toolkit → Trains adapter from JSONL files

**Key Files:**
- Shared config: `training_config.py` (systemPrompt, TOOL_DEFINITION)
- Output: `datasets/{set_name}/train.jsonl`, `valid.jsonl`, `test.jsonl`

---

## Pipeline Stages

### Stage 0: Prerequisites
**Input:** `widget_list.json` (downloaded from Übersicht GitHub repo)  
**Output:** None  
**Status:** Manual setup required

---

### Stage 1: Data Collection
**Script:** `downloadfullarchive.py`  
**Input:** `widget_list.json`  
**Output:** `downloads/{widget_folder}/` (extracted widget archives)

**Purpose:** Downloads and extracts widget ZIP files from URLs in the manifest.

**Key Operations:**
- Reads `widget_list.json` manifest
- Downloads ZIP archives for each widget
- Extracts to `downloads/{widget_id}/` or `downloads/{widget_folder}/`
- Creates widget folder structure with JSX files

**Dependencies:** None  
**Next Stage:** Stage 2

---

### Stage 2: Widget Analysis
**Script:** `generate_widget_report.py`  
**Input:** `downloads/` directory, `widget_list.json`  
**Output:** `widget_processing_results.csv`

**Purpose:** Analyzes downloaded widgets and generates metadata CSV.

**Key Operations:**
- Scans `downloads/` for CoffeeScript files (`PS_iscoffee`)
- Detects JSX usage (`PS_isJSX = "Y"`)
- Extracts widget folder paths (`PS_widgetfoldername`)
- Combines original manifest data with analysis results
- Writes comprehensive CSV with all metadata

**CSV Columns Generated:**
- `OS_*` (Original Source): From `widget_list.json`
- `PS_*` (Processing Status): Analysis results
  - `PS_iscoffee`: Y/N
  - `PS_isJSX`: Y/N  
  - `PS_widgetfoldername`: Relative path in downloads/

**Dependencies:** Stage 1 must complete  
**Next Stage:** Stage 3

---

### Stage 3: Prompt Generation
**Script:** (Manual or AI-assisted)  
**Input:** `widget_processing_results.csv`, `downloads/` directory  
**Output:** `prompts/{widget_id}.prompt` files

**Purpose:** Generate user prompts that describe what each widget should do.

**Key Operations:**
- For each JSX widget (`PS_isJSX = "Y"`):
  1. Read widget description from CSV (`OS_description`)
  2. Analyze JSX code structure in `downloads/{PS_widgetfoldername}/`
  3. Generate comprehensive prompt describing widget functionality
  4. Save to `prompts/{widget_id}.prompt`

**Prompt Format:**
```
Create an Übersicht widget that [OS_description]. 
The widget should [key functionality from JSX analysis] 
using React/JSX with [styling approach].
```

**Prompt Variations for Training Diversity:**

To reduce bias toward "Create an Übersicht widget" language and improve model generalization, consider using diverse opening phrases. Here are 52 variations organized by category:

**Direct Action Verbs:**
1. `Create an Übersicht widget that`
2. `Build an Übersicht widget that`
3. `Make an Übersicht widget that`
4. `Design an Übersicht widget that`
5. `Generate an Übersicht widget that`
6. `Build me an Übersicht widget that`
7. `Create a widget that`
8. `Build a widget that`
9. `Make a widget that`
10. `Design a widget that`

**Indirect Requests:**
11. `I need an Übersicht widget that`
12. `I want an Übersicht widget that`
13. `I'd like an Übersicht widget that`
14. `I need a widget that`
15. `I want a widget that`
16. `I'd like a widget that`
17. `I'm looking for an Übersicht widget that`
18. `I'm looking for a widget that`

**Question Forms:**
19. `Can you create an Übersicht widget that`
20. `Can you build an Übersicht widget that`
21. `Can you make an Übersicht widget that`
22. `Can you design an Übersicht widget that`
23. `Could you create an Übersicht widget that`
24. `Could you build an Übersicht widget that`
25. `Would you create an Übersicht widget that`
26. `Can you create a widget that`
27. `Can you build a widget that`
28. `Can you make a widget that`

**Descriptive Starts (No Explicit "Create"):**
29. `An Übersicht widget that`
30. `A widget that`
31. `Show me an Übersicht widget that`
32. `Show me a widget that`
33. `Display an Übersicht widget that`
34. `Display a widget that`
35. `Give me an Übersicht widget that`
36. `Give me a widget that`

**Imperative/Command Forms:**
37. `Build an Übersicht widget for`
38. `Make an Übersicht widget for`
39. `Create an Übersicht widget for`
40. `Design an Übersicht widget for`

**Action-Focused:**
41. `Generate a widget that`
42. `Produce an Übersicht widget that`
43. `Develop an Übersicht widget that`
44. `Implement an Übersicht widget that`

**Contextual Starts:**
45. `I'm building an Übersicht widget that`
46. `I'm making an Übersicht widget that`
47. `I'm creating an Übersicht widget that`
48. `I'm designing an Übersicht widget that`

**Casual/Informal:**
49. `Whip up an Übersicht widget that`
50. `Put together an Übersicht widget that`
51. `Come up with an Übersicht widget that`
52. `Make me an Übersicht widget that`

**Recommended Distribution:**
- 30-40%: Direct action verbs (1-10)
- 20-25%: Indirect requests (11-18)
- 15-20%: Question forms (19-28)
- 10-15%: Descriptive starts (29-36)
- 5-10%: Others (37-52)

**Dependencies:** Stage 2 must complete  
**Next Stage:** Stage 4 (optional) or Stage 5

---

### Stage 4: Size Evaluation (Optional but Recommended)
**Scripts:** 
- `evaluate_training_data_size.py` ⭐ **CRITICAL** - Evaluates complete training examples, generates strategy file
- `analyze_widget_sizes.py` 📊 **OPTIONAL** - Widget code only (nice-to-have)

**Input:** 
- `widget_processing_results.csv`
- `downloads/` directory
- `prompts/` directory
- `training_config.py` (for systemPrompt and tool definitions)

**Output:** 
- `training_data_size_analysis.json` ⭐ (detailed analysis)
- `training_data_strategy.json` ⭐ **ACTIONABLE** (strategy for create_dataset.py)
- `widget_size_analysis.json` 📊 (from optional script)
- Console recommendations with specific widget actions

**Purpose:** Evaluate which training examples exceed `max_sequence_length` limits and generate actionable strategy recommendations for `create_dataset.py`.

#### `evaluate_training_data_size.py` ⭐ **CRITICAL**
**Status:** Use this to evaluate training data size and generate actionable strategy before generating datasets.

- Evaluates **complete training examples** including:
  - System prompt tokens
  - Tool definition tokens
  - User prompt tokens
  - Widget code tokens
  - JSON structure overhead
- Uses same `systemPrompt` and `TOOL_DEFINITION` from `training_config.py`
- Builds exact JSON structure that will be generated
- Provides accurate token counts for actual training data
- **Generates actionable strategy file** (`training_data_strategy.json`) that specifies:
  - Which widgets to **keep** as-is (fit within token limit)
  - Which widgets to **exclude** (exceed token limit, with reason)
- **Required** for making informed decisions and implementing strategy in `create_dataset.py`

#### Strategy File Structure (`training_data_strategy.json`)

The strategy file generated by `evaluate_training_data_size.py` has the following structure:

**Top-Level Properties:**
- `max_sequence_length` (integer): The token limit used for evaluation (default: 4095)
- `strategy` (object): Maps widget IDs to their individual strategy entries
- `summary` (object): Aggregated counts by action type

**Per-Widget Strategy Properties:**
Each widget in the `strategy` object contains:

- `action` (string): Required. One of:
  - `"keep"`: Widget fits within token limit, include as-is
  - `"exclude"`: Widget exceeds token limit, skip entirely
- `current_total_tokens` (integer): Estimated total tokens for the complete training example (system + tool def + user prompt + widget code + JSON overhead)
- `current_widget_tokens` (integer): Estimated tokens for widget code only (JSX portion)

**Properties for "exclude" actions only:**
- `reason` (string): Human-readable explanation for exclusion (e.g., "Exceeds limit (5286 > 4095 tokens)")
- `over_by` (integer): How many tokens the widget exceeds the limit

**Example Structure:**
```json
{
  "max_sequence_length": 4095,
  "strategy": {
    "widget-id-1": {
      "action": "keep",
      "current_total_tokens": 2347,
      "current_widget_tokens": 1417
    },
    "widget-id-2": {
      "action": "exclude",
      "reason": "Exceeds limit (5286 > 4095 tokens)",
      "current_total_tokens": 5286,
      "current_widget_tokens": 4233,
      "over_by": 1191
    }
  },
  "summary": {
    "keep": 64,
    "exclude": 11
  }
}
```

**Usage in `create_dataset.py`:**
- Reads `training_data_strategy.json` if it exists (optional - script works without it)
- For each widget, checks `action` property:
  - If `"exclude"`: Skips widget and logs reason
  - If `"keep"` or not in strategy: Processes widget normally
- Other properties (`current_total_tokens`, `reason`, etc.) are informational for debugging

#### `analyze_widget_sizes.py` 📊 **OPTIONAL (Nice-to-Have)**
**Status:** Optional tool for quick widget-only analysis.

- Analyzes widget code size only (JSX files in `downloads/`)
- Estimates tokens for JSX files
- Identifies widgets that may be too large
- Provides basic exclusion/truncation recommendations
- **Note:** Less accurate than full analysis - doesn't account for system prompts, user prompts, or JSON overhead
- **Use Case:** Quick preliminary check before prompts exist, or to see raw widget sizes

**Recommendations Provided:**
1. **Exclusion Strategy:** Remove large examples
2. **Truncation Strategy:** Cut to fit max_sequence_length
3. **Hybrid Strategy:** Exclude extreme, truncate moderate
4. **Chunking Strategy:** Split large widgets (complex)

**Dependencies:** Stages 2 and 3 must complete  
**Next Stage:** Stage 5 (with strategy adjustments to `create_dataset.py`)

---

### Stage 5: Dataset Generation
**Script:** `create_dataset.py`  
**Input:** 
- `widget_processing_results.csv`
- `prompts/{widget_id}.prompt` files
- `downloads/{PS_widgetfoldername}/` widget code
- `systemPrompt` (defined in script)
- `TOOL_DEFINITION` (defined in script)

**Output:** `datasets/{set_name}/train.jsonl`, `valid.jsonl`, `test.jsonl`

**Purpose:** Generate Apple adapter training dataset in JSONL format matching Apple's schema.md.

**Key Operations:**
1. **Filter JSX widgets** from CSV (`PS_isJSX = "Y"`)
2. **Read user prompts** from `prompts/{widget_id}.prompt`
3. **Load widget code** from `downloads/{PS_widgetfoldername}/`
   - Finds all `.jsx` files recursively
   - Concatenates with filename comments
4. **Build JSON structure** for each training example:
   ```json
   [
     {
       "role": "system",
       "content": systemPrompt,
       "tools": [TOOL_DEFINITION]
     },
     {
       "role": "user", 
       "content": "{prompt from prompts/}"
     },
     {
       "role": "assistant",
       "content": "{complete widget JSX code}"
     }
   ]
   ```
5. **Split dataset** 80/10/10 (train/valid/test)
6. **Write JSONL files** (one JSON array per line)

**Current Configuration:**
- System prompt includes tool calling instructions
- Tool definition in system message
- Full widget code in assistant `content` (no `tool_calls` in assistant)
- Matches Apple's schema.md format

**Potential Enhancements** (based on Stage 4 analysis):
- Add exclusion logic for oversized widgets
- Add truncation logic for moderately large widgets
- Add chunking logic for extreme widgets

**Dependencies:** Stages 2, 3, and optionally 4  
**Next Stage:** Stage 6

---

### Stage 6: Model Training
**Script:** (External: Apple's adapter training toolkit)  
**Input:** `datasets/{set_name}/*.jsonl` files  
**Output:** Trained adapter weights

**Purpose:** Fine-tune adapter on generated training data.

**Configuration Used:**
```python
AdapterTrainingConfiguration(
    epochs=6,
    learning_rate=0.0001,
    batch_size=1,
    max_sequence_length=4095,  # Must be < 4096
    # ... other params
)
```

**Dependencies:** Stage 5 must complete  
**Output:** Trained adapter model

---

## Data Flow Diagram

```
widget_list.json
    ↓
[downloadfullarchive.py]
    ↓
downloads/{widget}/
    ↓
[generate_widget_report.py]
    ↓
widget_processing_results.csv
    ↓
[Prompt Generation - Manual/AI]
    ↓
prompts/{widget_id}.prompt
    ↓
[evaluate_training_data_size.py] ← training_config.py (reads systemPrompt, TOOL_DEFINITION)
    ↓
training_data_strategy.json (actionable strategy for create_dataset.py)
    ↓
[create_dataset.py] ← Uses systemPrompt, TOOL_DEFINITION from training_config.py
                       ← Optionally uses training_data_strategy.json for exclude actions
    ↓
datasets/{set_name}/
    ├── train.jsonl
    ├── valid.jsonl
    └── test.jsonl
    ↓
[Apple Training Toolkit]
    ↓
Trained Adapter Model
```

## Key Data Structures

### CSV Structure (`widget_processing_results.csv`)
- **OS_***: Original source data from manifest
- **PS_***: Processing status (analysis results)
- **AI_***: AI-generated data (categories, prompts)
- **CT_***: Curation task decisions

### JSONL Structure (Training Data)
Each line = one training example as JSON array:
```json
[
  {"role": "system", "content": "...", "tools": [...]},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."}
]
```

## Configuration Sharing

**Shared Configuration:** `training_config.py` contains:
- `systemPrompt` string
- `TOOL_DEFINITION` structure

**Used By:**
- `create_dataset.py` - imports from `training_config`
- `analyze_training_data_size.py` - imports from `training_config`

**Benefits:**
- Single source of truth for prompt and tool definition
- Easy to update - change once, affects both scripts
- Ensures consistency between analysis and generation

## Script Dependencies Summary

| Script | Status | Depends On | Outputs To |
|--------|--------|-----------|-----------|
| `downloadfullarchive.py` | ⭐ Critical | `widget_list.json` | `downloads/` |
| `generate_widget_report.py` | ⭐ Critical | `downloads/`, `widget_list.json` | `widget_processing_results.csv` |
| Prompt Generation | ⭐ Critical | `widget_processing_results.csv`, `downloads/` | `prompts/` |
| `evaluate_training_data_size.py` | ⭐ Critical | `widget_processing_results.csv`, `downloads/`, `prompts/`, `training_config.py` | `training_data_size_analysis.json`, `training_data_strategy.json` |
| `analyze_widget_sizes.py` | 📊 Optional | `widget_processing_results.csv`, `downloads/` | `widget_size_analysis.json` |
| `create_dataset.py` | ⭐ Critical | `widget_processing_results.csv`, `prompts/`, `downloads/` | `datasets/{set_name}/*.jsonl` |

## Typical Workflow

1. **Initial Setup:**
   ```bash
   python3 downloadfullarchive.py
   python3 generate_widget_report.py
   ```

2. **Generate Prompts:**
   (Manual process or AI-assisted for missing prompts)

3. **Evaluate Sizes (Recommended):**
   ```bash
   python3 evaluate_training_data_size.py --csv widget_processing_results.csv
   ```
   (Optional: `python3 analyze_widget_sizes.py` for widget-only quick check)
   - Generates `training_data_strategy.json` with specific actions for each widget

4. **Implement Strategy** (if needed):
   - Review `training_data_strategy.json` recommendations
   - Strategy is automatically applied by `create_dataset.py` (reads JSON and applies exclude actions)

5. **Generate Dataset:**
   ```bash
   python3 create_dataset.py --csv widget_processing_results.csv --set my_dataset_v1 --system-prompt systemPrompt_v6
   ```

6. **Train Model:**
   (Use Apple's adapter training toolkit with generated JSONL files)

---

## Command-Line Reference

### `downloadfullarchive.py`
Download and extract widget archives.

**Basic usage:**
```bash
python3 downloadfullarchive.py
```

**With specific widgets:**
```bash
# Download specific widgets by ID
python3 downloadfullarchive.py --widgets widget1,widget2,widget3

# Download widgets from a file (one ID per line)
python3 downloadfullarchive.py --widget-file my_widgets.txt
```

---

### `generate_widget_report.py`
Analyze downloaded widgets and generate metadata CSV.

**Usage:**
```bash
python3 generate_widget_report.py
```

**Note:** This script uses default paths (`downloads/`, `widget_list.json`) and outputs `widget_processing_results.csv`.

---

### `evaluate_training_data_size.py` ⭐
Evaluate complete training data size and generate strategy recommendations.

**Basic usage:**
```bash
python3 evaluate_training_data_size.py
```

**Full options:**
```bash
python3 evaluate_training_data_size.py \
  --csv widget_processing_results.csv \
  --downloads downloads \
  --prompts prompts \
  --max-tokens 4095
```

**Outputs:**
- `training_data_size_analysis.json` - Detailed analysis
- `training_data_strategy.json` - Actionable strategy (keep/exclude) for `create_dataset.py`
- Console output with summary and recommendations

---

### `analyze_widget_sizes.py` 📊 (Optional)
Quick widget-only size analysis (doesn't include prompts/system messages).

**Usage:**
```bash
python3 analyze_widget_sizes.py \
  --csv widget_processing_results.csv \
  --downloads downloads \
  --max-tokens 4095
```

---

### `create_dataset.py` ⭐
Generate JSONL training/validation/test datasets.

**Required arguments:**
```bash
python3 create_dataset.py \
  --csv widget_processing_results.csv \
  --set my_dataset_v1
```

**Output:** Creates `datasets/my_dataset_v1/train.jsonl`, `valid.jsonl`, `test.jsonl`

**Note:** Uses `systemPrompt` and `TOOL_DEFINITION` from `training_config.py`.

---

## Notes

- All scripts should use consistent encoding (UTF-8)
- Error handling skips missing files with warnings
- JSONL format follows Apple's schema.md specification
- System prompt and tool definitions must match between analysis and generation scripts

hell'