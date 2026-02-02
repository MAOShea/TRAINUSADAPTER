# Summary: Training Adapter for Tool Calling

## The Goal
Train a custom adapter model that can **call tools** (specifically `WriteUbersichtWidgetToFileSystem`) instead of just generating JSX code.

## The Problem
Your adapter was trained to generate JSX code but **not to call tools**. The base model works fine with tool calling, but the adapter doesn't.

## What We've Done

### **1. Modified Training Data Generation**
- **Added `tool_calls`** to assistant responses in training data
- **Using complete widget code** as `jsxContent` parameter (no parameter extraction)
- **Simplified system prompt** (`systemPrompt_v7`) - minimal, stripped-down approach per Apple dev support recommendations
- **Tool definition** includes `WriteUbersichtWidgetToFileSystem` with `jsxContent` parameter
- **JSONL validation** added to ensure all generated files are valid

### **2. Current Status**
- **Script generates tool calls** ✅
- **Uses `systemPrompt_v7`** from `training_config.py` ✅
- **Complete JSX code** passed as `jsxContent` in tool calls ✅
- **Training data format** follows OpenAI standard with `tool_calls` array ✅
- **JSONL files validated** after generation ✅

## What Needs to Be Done

### **1. Generate New Dataset**
- **Run `create_dataset.py`** with the new simplified system prompt (use the `--system-prompt` flag)
- **Verify tool calls** are generated correctly in JSONL files

### **2. Train the Adapter**
- **Train new adapter** with the simplified prompt dataset
- **Test tool calling** in your Swift app
- **Verify adapter calls tools** correctly with the stripped-down prompt

## Key Files
- **`create_dataset.py`** - Script to generate training data (uses `systemPrompt_v7`)
- **`training_config.py`** - Contains `systemPrompt_v7` (simplified) and `TOOL_DEFINITION`
- **JSX widget files** - Source code to parse (from `downloads/` folder)
- **CSV files** - Training data source (`widget_processing_results.csv`)
- **Generated JSONL** - Training datasets with tool calls (in `datasets/{set_name}/`)

## The End Goal
An adapter that learns to **call the WriteUbersichtWidgetToFileSystem tool** with proper parameters, just like your base model does, but with better JSX generation quality.

---

## History / Development Diary

### Previous Approach (Superseded)

**Old Status (Before Simplified Prompt):**
- **Script generates tool calls** ✅
- **Some parameters extracted** (CSS positioning, some bash commands)
- **`renderFunction` still empty** ❌ - regex pattern needed fixing
- **`refreshFrequency` now defaults to 1000** ✅

**Previous Parameter Extraction Approach:**
- **Created extraction functions** to parse JSX code and extract 4 parameters:
  - `bashCommand` (string)
  - `refreshFrequency` (integer) 
  - `renderFunction` (string)
  - `cssPositioning` (string)

**Previous TODO Items (No Longer Needed):**
1. ~~Fix Regex Patterns~~ - No longer extracting individual parameters
2. ~~Improve Training Data~~ - Now using complete JSX code directly
3. ~~Better parameter extraction~~ - Simplified to use full `jsxContent`

**Note:** Apple dev support recommended a stripped-down system prompt approach, leading to the current simplified implementation using `systemPrompt_v7`.
