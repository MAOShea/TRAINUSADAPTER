# System Prompt ↔ Dataset ↔ Adapter Map

This table lists each system prompt key from `system_prompts.json`, its id/date, the matching dataset folder (if present in `datasets/`), and the adapter model name used when exporting with the notebook convention `adapter_{DATA_SET}`. Update the adapter name column if you used a different naming scheme.

| System prompt id | System prompt key | System prompt date | Dataset folder | Adapter model name |
| --- | --- | --- | --- | --- |
| 1 | my_dataset_v1 | 2025-10-04T19:46:23.408274 | my_dataset_v1 | adapter_my_dataset_v1 |
| 2 | debug_check | 2025-10-05T10:13:30.683180 | debug_check | adapter_debug_check |
| 3 | test_complete | 2025-10-05T10:47:22.620862 | test_complete | adapter_test_complete |
| 4 | withtoolcall | 2025-10-24T18:09:09.598217 | withtoolcall | adapter_withtoolcall |
| 5 | withtoolcall2 | 2025-10-26T18:46:28.772158 | withtoolcall2 | adapter_withtoolcall2 |
| 6 | withtoolcall3 | 2025-10-27T14:35:03.181164 | withtoolcall3 | adapter_withtoolcall3 |
| 7 | toolcall_plus_notruncation | 2025-10-31T14:25:07.746244 | toolcall_plus_notruncation | adapter_toolcall_plus_notruncation |
| 8 | with_tool_calls | 2025-11-03T16:55:01.503391 | with_tool_calls | adapter_with_tool_calls |
| 9 | with_tool_calls_2 | 2025-11-03T17:34:13.257582 | with_tool_calls_2 | adapter_with_tool_calls_2 |
| 10 | with_tool_calls_3 | 2025-11-03T18:26:18.042937 | with_tool_calls_3 | adapter_with_tool_calls_3 |
| 11 | with_tool_calls_4 | 2025-11-03T18:34:28.701646 | with_tool_calls_4 | adapter_with_tool_calls_4 |
| 12 | fixed_create_directive_bias | 2025-11-05T11:37:52.525559 | fixed_create_directive_bias | adapter_fixed_create_directive_bias |
| 13 | API_props_are_optional | 2025-11-05T14:40:43.286591 | API_props_are_optional | adapter_API_props_are_optional |
| 13.1 | systemPrompt_v1 | 2025-12-20T19:41:04.000000 | — | — |
| 13.2 | systemPrompt_v2 | 2025-12-20T19:41:04.000000 | — | — |
| 13.3 | systemPrompt_v3 | 2025-12-20T19:41:04.000000 | — | — |
| 13.4 | systemPrompt_v4 | 2025-12-20T19:41:04.000000 | — | — |
| 13.5 | systemPrompt_v5 | 2025-12-20T19:41:04.000000 | systemPrompt_v5 | adapter_systemPrompt_v5 |
| 14 | systemPrompt_v6 | 2026-01-17T15:17:21.694896 | — | — |
