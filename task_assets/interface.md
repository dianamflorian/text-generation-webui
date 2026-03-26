## Public Interface

---
**Path:** repo/modules/reasoning.py
**Name:** THINKING_FORMATS
**Type:** constant (list of tuples)
**Input:** N/A
**Output:** list[tuple[str | None, str, str | None]]
**Description:** Module-level list of `(start_tag, end_tag, content_tag)` tuples defining all recognized thinking-block formats. Used by `extract_reasoning` to detect and parse thinking/reasoning sections.

---
**Path:** repo/modules/reasoning.py
**Name:** extract_reasoning
**Type:** function
**Input:** text: str, html_escaped: bool = False
**Output:** tuple[str | None, str]
**Description:** Extracts a reasoning/thinking block from the beginning of `text`. Returns `(reasoning_content, final_content)`. `reasoning_content` is `None` if no recognized thinking block is found. When `html_escaped=True`, tags are HTML-escaped before matching (for use on already-escaped UI strings).

---
**Path:** repo/modules/sane_markdown_lists.py
**Name:** MIN_NESTED_LIST_INDENT
**Type:** constant (int)
**Input:** N/A
**Output:** int
**Description:** Minimum number of spaces required to indent a nested list item. Value is 2 and must be > 1.

---
**Path:** repo/modules/sane_markdown_lists.py
**Name:** SaneListExtension
**Type:** class (extends markdown.Extension)
**Input:** N/A
**Output:** N/A
**Description:** Python-Markdown extension that replaces the standard list processors with sane variants. Pass an instance to `markdown.markdown(..., extensions=[SaneListExtension()])`.

---
**Path:** repo/modules/sane_markdown_lists.py
**Name:** SaneListExtension.extendMarkdown
**Type:** method
**Input:** self, md: markdown.Markdown
**Output:** None
**Description:** Registers `SaneListIndentProcessor`, `SaneOListProcessor`, `SaneUListProcessor`, and `SaneParagraphProcessor` into the markdown instance, and deregisters the built-in `code` block processor.

---
**Path:** repo/modules/sane_markdown_lists.py
**Name:** makeExtension
**Type:** function
**Input:** **kwargs
**Output:** SaneListExtension
**Description:** Factory function required by Python-Markdown's extension loading protocol. Returns a new `SaneListExtension` instance.

---
**Path:** repo/modules/logging_colors.py
**Name:** logger
**Type:** global variable (logging.Logger)
**Input:** N/A
**Output:** logging.Logger
**Description:** Module-level logger named `'text-generation-webui'`. Imported by `utils.py`, `shared.py`, and `presets.py` for all log output.

---
**Path:** repo/modules/paths.py
**Name:** resolve_user_data_dir
**Type:** function
**Input:** (none)
**Output:** pathlib.Path
**Description:** Resolves the user data directory path. Precedence: `--user-data-dir` CLI flag → `../user_data` in portable mode → `Path('user_data')` default. Called at module level in `shared.py`.

---
**Path:** repo/modules/shared.py
**Name:** user_data_dir
**Type:** global variable (pathlib.Path)
**Input:** N/A
**Output:** pathlib.Path
**Description:** Resolved path to the user data directory. Accessed by `html_generator.py` (for image cache), `utils.py`, and `presets.py`.

---
**Path:** repo/modules/shared.py
**Name:** args
**Type:** global variable (argparse.Namespace)
**Input:** N/A
**Output:** argparse.Namespace
**Description:** Parsed CLI arguments. Accessed by `html_generator.py` (`args.disk_cache_dir`), `utils.py`, and `presets.py` (`args.portable`).

---
**Path:** repo/modules/shared.py
**Name:** settings
**Type:** global variable (dict)
**Input:** N/A
**Output:** dict
**Description:** Dictionary of runtime UI settings (chat style, mode, sampler values, etc.). Populated at module level with defaults from `default_preset()`.

---
**Path:** repo/modules/presets.py
**Name:** default_preset_values
**Type:** global variable (dict)
**Input:** N/A
**Output:** dict
**Description:** Dictionary of default sampler parameter values (temperature, top_p, top_k, etc.). Used to initialise `shared.settings` and referenced by `shared.py` argument parser defaults.

---
**Path:** repo/modules/presets.py
**Name:** default_preset
**Type:** function
**Input:** (none)
**Output:** dict
**Description:** Returns a copy of `default_preset_values`, optionally filtering sampler list when `shared.args.portable` is set. Called at module level in `shared.py` to build `neutral_samplers`.

---
**Path:** repo/modules/utils.py
**Name:** get_available_chat_styles
**Type:** function
**Input:** (none)
**Output:** list[str]
**Description:** Returns a sorted list of available chat style names by globbing `css/chat_style*.css` in the current working directory. Called at module level in `html_generator.py` to populate `chat_styles`.

---
**Path:** repo/modules/html_generator.py
**Name:** image_cache
**Type:** global variable (dict)
**Input:** N/A
**Output:** dict
**Description:** Module-level cache mapping image `Path` objects to `[mtime, output_path_str]`. Used by `get_image_cache`.

---
**Path:** repo/modules/html_generator.py
**Name:** convert_to_markdown
**Type:** function
**Input:** string: str, message_id: str | None = None
**Output:** str
**Description:** Converts a raw message string to HTML, handling tool-call blocks, thinking blocks, and markdown. Result is LRU-cached by `(string, message_id)`. Returns `""` for empty/None input.

---
**Path:** repo/modules/html_generator.py
**Name:** convert_to_markdown_wrapped
**Type:** function
**Input:** string: str, message_id: str | None = None, use_cache: bool = True
**Output:** str
**Description:** Wrapper around `convert_to_markdown` that bypasses the LRU cache when `use_cache=False` (used during streaming of the last message).

---
**Path:** repo/modules/html_generator.py
**Name:** generate_basic_html
**Type:** function
**Input:** string: str
**Output:** str
**Description:** Clears the markdown cache, converts `string` to markdown HTML, and wraps the result in a `<style>` tag with the readable CSS and a `<div class="readable-container">`.

---
**Path:** repo/modules/html_generator.py
**Name:** generate_instruct_html
**Type:** function
**Input:** history: dict, last_message_only: bool = False
**Output:** str
**Description:** Generates the full instruct-mode HTML for a chat history dict with `visible` and `internal` lists of `[user_text, assistant_text]` pairs.

---
**Path:** repo/modules/html_generator.py
**Name:** generate_cai_chat_html
**Type:** function
**Input:** history: dict, name1: str, name2: str, style: str, character: str, reset_cache: bool = False, last_message_only: bool = False
**Output:** str
**Description:** Generates the full CAI-style chat HTML for a history dict. `style` must be a key present in the `chat_styles` dict.

---
**Path:** repo/modules/html_generator.py
**Name:** chat_html_wrapper
**Type:** function
**Input:** history: dict, name1: str, name2: str, mode: str, style: str, character: str, reset_cache: bool = False, last_message_only: bool = False
**Output:** dict
**Description:** Top-level entry point. Dispatches to `generate_instruct_html` when `mode == 'instruct'`, otherwise to `generate_cai_chat_html`. Returns `{'html': str, 'last_message_only': bool}`.
