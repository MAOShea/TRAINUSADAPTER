# Troubleshooting Test Suite

This document tracks systematic testing of different system prompts against a standard set of user prompts to identify what works and what doesn't.

## Test Cases (User Prompts)

These are the standard prompts we test against:

1. **Simple Widget**: `"create a widget that says 'doodlebug'"`
2. **Time Widget**: `"create a widget that shows the current time"`
3. **System Info**: `"generate a widget that displays system information"`
4. **Multi-turn Conversation**: 
   - Turn 1: `"generate a widget that says 'abc as easy as 123'"`
   - Turn 2: `"move it to the top-right corner"`
5. **[Add more test cases here]**

---

## System Prompt Versions

### System Prompt v1.0
**Source:** `humanRolePrompt2` from `/Users/mike/Documents/hwta/Hello World Tools/Hello World Tools/Sources/Utilities/Constants.swift`

**Content:**
```
You are an Übersicht widget designer. Create Übersicht widgets when requested by the user.

IMPORTANT: You have access to a tool called WriteUbersichtWidgetToFileSystem. When asked to create a widget, you MUST call this tool.

### Tool Usage:
Call WriteUbersichtWidgetToFileSystem with complete JSX code that implements the Übersicht Widget API. Generate custom JSX based on the user's specific request - do not copy the example below.

### Übersicht Widget API (REQUIRED):
Every Übersicht widget MUST export these 4 items:
- export const command: The bash command to execute (string)
- export const refreshFrequency: Refresh rate in milliseconds (number)
- export const render: React component function that receives {output} prop (function)
- export const className: CSS positioning for absolute placement (string)

Example format (customize for each request):
WriteUbersichtWidgetToFileSystem({"jsxContent": "export const command = \"echo hello\"; export const refreshFrequency = 1000; export const render = ({output}) => { return <div>{output}</div>; }; export const className = \"top: 20px; left: 20px;\";"})

### Rules:
- The terms "ubersicht widget", "widget", "a widget", "the widget" must all be interpreted as "Übersicht widget"
- Generate complete, valid JSX code that follows the Übersicht widget API
- When you generate a widget, don't just show JSON or code - you MUST call the WriteUbersichtWidgetToFileSystem tool
- Report the results to the user after calling the tool

### Examples:
- "Generate a Übersicht widget" → Use WriteUbersichtWidgetToFileSystem tool
- "Can you add a widget that shows the time" → Use WriteUbersichtWidgetToFileSystem tool
- "Create a widget with a button" → Use WriteUbersichtWidgetToFileSystem tool
```

**Notes:**
- Uses "REQUIRED" language (all 4 exports mandatory)
- Single-line example format
- No modification support
- ✅ **Known to work** - correctly calls tool

---

### System Prompt v2.0
**Source:** `systemPrompt` from `/Users/mike/Documents/TrainUSAdapter/training_config.py`

**Content:**
```
A conversation between a user and a helpful assistant. You are an Übersicht widget designer. Create Übersicht widgets when requested by the user.

IMPORTANT: You have access to a tool called WriteUbersichtWidgetToFileSystem. You MUST call this tool whenever:
- Creating a new widget
- Modifying or updating an existing widget
- Making any changes to widget code requested by the user

### Tool Usage:
Call WriteUbersichtWidgetToFileSystem with complete JSX code that implements the Übersicht Widget API. 
- For new widgets: Generate custom JSX based on the user's specific request
- For modifications: Generate the updated/complete widget code incorporating the requested changes
Always provide the complete, final widget code - do not copy the example below.

### Übersicht Widget API:
Übersicht widgets should export at least one of these properties (all are optional, but most widgets use them):
- export const command: The bash command to execute (string or function). Optional - if refreshFrequency is false, command is not needed.
- export const refreshFrequency: Refresh rate in milliseconds (number). Optional - defaults to 1000ms if not provided. Can be set to false to disable auto-refresh.
- export const render: React component function that receives props (function). Optional - defaults to returning output if not provided.
- export const className: CSS positioning for absolute placement (string or object). Optional - used for positioning/styling the widget.

IMPORTANT: Use "export const" syntax, NOT comments. Each export must be on its own line with proper syntax.

Example format (customize for each request):
WriteUbersichtWidgetToFileSystem({"jsxContent": "export const command = \"echo hello\";\nexport const refreshFrequency = 1000;\nexport const render = ({output}) => {\n  return <div>{output}</div>;\n};\nexport const className = \"top: 20px; left: 20px;\";"})

### Rules:
- The terms "ubersicht widget", "widget", "a widget", "the widget" must all be interpreted as "Übersicht widget"
- Generate complete, valid JSX code that follows the Übersicht widget API
- When you create OR modify a widget, you MUST call the WriteUbersichtWidgetToFileSystem tool with the complete updated code
- For modifications: Generate the full widget code with all changes incorporated, then call the tool
- Report the results to the user after calling the tool

### Examples:
- "Generate a Übersicht widget" → Use WriteUbersichtWidgetToFileSystem tool
- "Can you add a widget that shows the time" → Use WriteUbersichtWidgetToFileSystem tool
- "Create a widget with a button" → Use WriteUbersichtWidgetToFileSystem tool
- "Make the font bigger" → Generate updated widget code → Use WriteUbersichtWidgetToFileSystem tool
- "Change the color to blue" → Generate updated widget code → Use WriteUbersichtWidgetToFileSystem tool
- "Add a border to the widget" → Generate updated widget code → Use WriteUbersichtWidgetToFileSystem tool
```

**Notes:**
- Uses "optional" language (properties are optional)
- Multi-line example format with `\n`
- Includes modification support
- Includes "NOT comments" warning
- ❌ **Known issue** - does not call tool

---

## Test Results Matrix

| Test Case | System Prompt v1.0 | System Prompt v2.0 | Notes |
|-----------|-------------------|-------------------|-------|
| 1. "create a widget that says 'doodlebug'" | ✅ Tool called<br>✅ Format correct | ❌ Tool not called<br>❌ Comments instead of exports<br>❌ Truncated | [Add detailed results below] |
| 2. "create a widget that shows the current time" | [Result] | [Result] | |
| 3. "generate a widget that displays system information" | [Result] | [Result] | |
| 4. Multi-turn: "generate widget..." then "move it..." | ✅ Turn 1: Tool called<br>✅ Turn 2: Works | ✅ Turn 1: Tool called<br>❌ Turn 2: Context exceeded (3732/4096 tokens) | Context window overflow in multi-turn |

---

## Detailed Test Results

### Test Case 1: "create a widget that says 'doodlebug'"

#### System Prompt v1.0
**Model:** Base / Adapter: [dataset name]  
**Date:** [Date]

**Result:**
```
[Paste full output here]
```

**Analysis:**
- ✅ Tool called: Yes/No
- ✅ Format: Correct/Incorrect
- ✅ Complete: Yes/No (truncated?)
- Notes: [Observations]

---

#### System Prompt v2.0
**Model:** Base / Adapter: [dataset name]  
**Date:** [Date]

**Result:**
```
// command: function() { console.log('dibbly-doo'); };

// refreshFrequency: 1000 // in milliseconds

// render: function() { return `<div class=
```

**Analysis:**
- ❌ Tool called: No
- ❌ Format: Incorrect (comments instead of exports)
- ❌ Complete: No (truncated at `class=`)
- Notes: 
  - Uses `//` comments instead of `export const`
  - Wrong syntax (function declaration)
  - Truncated mid-string
  - Uses `console.log` instead of command string

---

### Test Case 4: Multi-turn Conversation - "generate a widget that says 'abc as easy as 123'" then "move it to the top-right corner"

#### System Prompt v2.0 (systemPrompt_v4)
**Model:** Adapter Model (dataset: fixed_create_directive_bias)  
**Date:** [Date]

**Turn 1 Results:**
- ✅ Tool called: Yes
- ❌ Format: Incorrect (imports instead of direct exports)
- ✅ Complete: Yes
- 📊 Context usage: ~42 tokens / 4096 (~1%)
- 📊 Response length: 169 characters

**Turn 1 JSX Generated:**
```
//# sourceMappingURL=widget.jsx
import { command, refreshFrequency, render, className } from 'uebersicht';
export { command, refreshFrequency, render, className };
```

**Turn 2 Results:**
- ❌ **Context window exceeded!**
- Error: `Content contains 3732 tokens, which exceeds the maximum allowed context size of 4096`
- 📊 Context usage: 3732 tokens / 4096 (~91%)
- Status: ❌ FAILED - Context window limit reached

**Analysis:**
- **Context Window Growth:** The context grew from ~42 tokens (Turn 1) to 3732 tokens (Turn 2) - a **~89x increase**
- **Root Cause:** In multi-turn conversations, all previous messages accumulate in the context window:
  1. System prompt + tool definition (~constant)
  2. Turn 1: User message + Assistant response with tool call (includes full JSX code)
  3. Turn 2: User message + (attempted) Assistant response
  
- **The Problem:** The tool call from Turn 1 contains the full JSX code in the `jsxContent` argument. Even though the JSX was only 163 characters, when combined with:
  - The full conversation history
  - The system prompt
  - The tool definition
  - The JSON structure of the tool call
  - The new user message for Turn 2
  
  The total context exceeds 4096 tokens.

- **Implications:**
  - Multi-turn conversations are not feasible with the current setup if tool calls include full widget code
  - Each turn adds the previous tool call's JSX content to the context
  - Even small widgets can cause context overflow in multi-turn scenarios
  - The base model test showed only ~1% usage after 2 turns, suggesting the adapter's tool call format is much more verbose

- **Potential Solutions:**
  1. **Truncate tool call history:** Don't include full JSX content from previous tool calls in context
  2. **Summarize previous turns:** Replace full tool call with a summary like "Widget created with command='echo abc', positioned at default location"
  3. **Increase context window:** If possible, use a larger context window (but 4096 is likely a hardware/API limit)
  4. **Single-turn only:** Accept that modifications must be done in a single turn with full widget code

---

### Test Case 2: "create a widget that shows the current time"

#### System Prompt v1.0
**Model:** [Base / Adapter]  
**Date:** [Date]

**Result:**
```
[Paste output here]
```

**Analysis:**
- Tool called: Yes/No
- Format: Correct/Incorrect
- Complete: Yes/No
- Notes: [Observations]

---

#### System Prompt v2.0
**Model:** [Base / Adapter]  
**Date:** [Date]

**Result:**
```
[Paste output here]
```

**Analysis:**
- Tool called: Yes/No
- Format: Correct/Incorrect
- Complete: Yes/No
- Notes: [Observations]

---

## Context Window Analysis

### Multi-Turn Conversation Context Growth

**Problem:** In multi-turn conversations, the context window grows rapidly because:
1. Each turn includes all previous messages
2. Tool calls contain full JSX code in their arguments
3. The JSON structure of tool calls adds overhead

**Example from Test Case 4:**
- **Turn 1:** ~42 tokens (~1% of 4096) ✅
- **Turn 2:** 3732 tokens (~91% of 4096) ❌ **EXCEEDED**

**Context Breakdown (estimated):**
- System prompt + tool definition: ~500-800 tokens
- Turn 1 user message: ~20 tokens
- Turn 1 assistant response with tool call: ~200-300 tokens (includes JSX)
- Turn 2 user message: ~15 tokens
- Turn 2 attempted response: ~2600+ tokens (estimated, but failed)

**Key Finding:** The adapter model's tool call format is much more verbose than the base model's format. The base model test showed only ~1% usage after 2 turns, while the adapter exceeded the limit.

**✅ ROOT CAUSE IDENTIFIED (Runtime Analysis):**

The adapter stores full tool call arguments (complete jsxContent JSON) in transcript entries because it was trained with full arguments in the training examples. FoundationModels matches the training format at inference, so it includes full arguments (~575 tokens per tool call vs ~146 tokens for the base model). This causes the adapter's conversation history to grow 3-4x faster, leading to context window exhaustion on turn 2 (3708/4096 tokens).

**Why Base Model Doesn't Have This Issue:**
- **Base model**: Uses a function calling API that stores tool calls compactly (tool name + minimal metadata, no full arguments)
- **Adapter model**: Uses the full JSON format as trained (with full arguments in `jsxContent`)

**Token Comparison:**
- **Base model tool call**: ~146 tokens (compact format)
- **Adapter model tool call**: ~575 tokens (full arguments included)
- **Growth rate**: Adapter grows 3-4x faster per turn

**Impact:**
- Multi-turn conversations are currently **not feasible** with adapter model
- Each tool call adds significant context overhead
- Even small widgets cause context overflow in multi-turn scenarios

**✅ SOLUTION (Confirmed):**

**Retrain the adapter with compact tool call format:**
- Include only the tool name/ID in training examples, not the full arguments JSON payload
- This will cause FoundationModels to store tool calls compactly at inference time
- Avoids context window issues in multi-turn conversations

**Implementation Required:**
- Modify `create_dataset.py` to generate training examples with compact tool calls (tool name/ID only, no `jsxContent` in arguments)
- Retrain adapter with new dataset format
- Verify that tool calls are stored compactly in conversation history

**Alternative Solutions (Not Recommended):**
1. **Truncate tool call history** - Don't include full JSX from previous tool calls (runtime workaround)
2. **Summarize previous turns** - Replace full tool calls with summaries (complex, error-prone)
3. **Single-turn only** - Accept that modifications must include full widget code in one turn (limits functionality)
4. **Increase context window** - If hardware/API allows (unlikely with 4096 limit)

---

## Summary

### System Prompt v1.0
- **Tool Calling:** ✅ Works
- **Format:** ✅ Correct
- **Issues:** [List any issues]

### System Prompt v2.0
- **Tool Calling:** ✅ Works (tool is called)
- **Format:** ❌ Incorrect (imports instead of direct exports)
- **Context Window:** ❌ Multi-turn conversations fail due to context overflow
- **Issues:** 
  - Model generates imports instead of direct exports
  - Multi-turn conversations exceed context window (3732/4096 tokens at turn 2)
  - Tool call format is verbose, causing rapid context growth

---

## Template for New Test Case

### Test Case N: "[User prompt]"

#### System Prompt vX.X
**Model:** [Base / Adapter: dataset name]  
**Date:** [Date]

**Result:**
```
[Paste full output here]
```

**Analysis:**
- Tool called: Yes/No
- Format: Correct/Incorrect
- Complete: Yes/No
- Notes: [Observations]

---

## Template for New System Prompt Version

### System Prompt vX.X
**Source:** [File path]  
**Date Created:** [Date]  
**Changes from vX.X-1:** [What changed]

**Content:**
```
[Full prompt content]
```

**Notes:**
- [Key characteristics]
- [Known issues/features]
