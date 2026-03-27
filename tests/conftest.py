"""Configure pytest: setup environment for html_generator tests."""
import sys
from pathlib import Path

# Patch sys.argv so shared.py's parser.parse_args() doesn't fail when
# pytest passes its own arguments (e.g. 'tests/ -v').
# This runs at collection time, before any test module is imported.
sys.argv = ['server.py']

# Create CSS files required by html_generator module-level open() calls.
# The files are opened relative to modules/html_generator.py's location.
_css_dir = Path(__file__).parent.parent / 'css'  # repo/css/
_css_dir.mkdir(exist_ok=True)

for _css_file in ['html_readable_style.css', 'html_instruct_style.css']:
    _p = _css_dir / _css_file
    if not _p.exists():
        _p.write_text('/* empty */')

# Create a default chat style so generate_cai_chat_html tests can work
_chat_style = _css_dir / 'chat_style-default.css'
if not _chat_style.exists():
    _chat_style.write_text('/* chat_style-default.css */')
