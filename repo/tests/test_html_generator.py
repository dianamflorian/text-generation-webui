"""End-to-end tests for modules.html_generator public interface."""
import pytest

# Import at module level - conftest.py creates CSS files before this is loaded.
from modules.html_generator import (
    image_cache,
    convert_to_markdown,
    convert_to_markdown_wrapped,
    generate_basic_html,
    generate_instruct_html,
    generate_cai_chat_html,
    chat_html_wrapper,
)


# ---------------------------------------------------------------------------
# image_cache
# ---------------------------------------------------------------------------

def test_image_cache_is_dict():
    assert isinstance(image_cache, dict)


# ---------------------------------------------------------------------------
# convert_to_markdown
# ---------------------------------------------------------------------------

def test_convert_to_markdown_empty_returns_empty():
    assert convert_to_markdown('') == ''


def test_convert_to_markdown_none_returns_empty():
    assert convert_to_markdown(None) == ''


def test_convert_to_markdown_returns_string():
    result = convert_to_markdown('Hello world')
    assert isinstance(result, str)


def test_convert_to_markdown_contains_text():
    result = convert_to_markdown('Hello world')
    assert 'Hello world' in result


def test_convert_to_markdown_with_message_id_returns_string():
    result = convert_to_markdown('Some text', message_id='msg-1')
    assert isinstance(result, str)


def test_convert_to_markdown_markdown_bold():
    """Bold markdown ** should produce HTML with the text present."""
    result = convert_to_markdown('**bold text**')
    assert 'bold text' in result


# ---------------------------------------------------------------------------
# convert_to_markdown_wrapped
# ---------------------------------------------------------------------------

def test_convert_to_markdown_wrapped_returns_string():
    result = convert_to_markdown_wrapped('hello')
    assert isinstance(result, str)


def test_convert_to_markdown_wrapped_no_cache_returns_string():
    result = convert_to_markdown_wrapped('hello', use_cache=False)
    assert isinstance(result, str)


def test_convert_to_markdown_wrapped_cache_matches_direct():
    text = 'cache consistency test'
    direct = convert_to_markdown(text)
    wrapped = convert_to_markdown_wrapped(text, use_cache=True)
    assert direct == wrapped


def test_convert_to_markdown_wrapped_empty_returns_empty():
    assert convert_to_markdown_wrapped('') == ''


# ---------------------------------------------------------------------------
# generate_basic_html
# ---------------------------------------------------------------------------

def test_generate_basic_html_returns_string():
    result = generate_basic_html('Test content')
    assert isinstance(result, str)


def test_generate_basic_html_has_style_tag():
    result = generate_basic_html('Test content')
    assert '<style>' in result


def test_generate_basic_html_has_readable_container():
    result = generate_basic_html('Test content')
    assert 'readable-container' in result


def test_generate_basic_html_empty_input():
    result = generate_basic_html('')
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# generate_instruct_html
# ---------------------------------------------------------------------------

def test_generate_instruct_html_returns_string():
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = generate_instruct_html(history)
    assert isinstance(result, str)


def test_generate_instruct_html_empty_history():
    history = {'visible': [], 'internal': []}
    result = generate_instruct_html(history)
    assert isinstance(result, str)


def test_generate_instruct_html_last_message_only():
    history = {
        'visible': [['q1', 'a1'], ['q2', 'a2']],
        'internal': [['q1', 'a1'], ['q2', 'a2']],
    }
    result = generate_instruct_html(history, last_message_only=True)
    assert isinstance(result, str)


def test_generate_instruct_html_contains_content():
    history = {'visible': [['question', 'answer']], 'internal': [['question', 'answer']]}
    result = generate_instruct_html(history)
    assert 'answer' in result


# ---------------------------------------------------------------------------
# generate_cai_chat_html
# ---------------------------------------------------------------------------

def test_generate_cai_chat_html_returns_string(monkeypatch):
    import modules.html_generator as hg
    monkeypatch.setitem(hg.chat_styles, 'default', '/* empty */')
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = generate_cai_chat_html(history, 'User', 'Bot', 'default', 'Bot')
    assert isinstance(result, str)


def test_generate_cai_chat_html_empty_history(monkeypatch):
    import modules.html_generator as hg
    monkeypatch.setitem(hg.chat_styles, 'default', '/* empty */')
    history = {'visible': [], 'internal': []}
    result = generate_cai_chat_html(history, 'User', 'Bot', 'default', 'Bot')
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# chat_html_wrapper
# ---------------------------------------------------------------------------

def test_chat_html_wrapper_returns_dict():
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert isinstance(result, dict)


def test_chat_html_wrapper_has_html_key():
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert 'html' in result


def test_chat_html_wrapper_html_is_string():
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert isinstance(result['html'], str)


def test_chat_html_wrapper_has_last_message_only_key():
    history = {'visible': [['hi', 'hello']], 'internal': [['hi', 'hello']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert 'last_message_only' in result


def test_chat_html_wrapper_empty_history():
    history = {'visible': [], 'internal': []}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert isinstance(result, dict)
    assert isinstance(result['html'], str)


def test_chat_html_wrapper_last_message_only_false_by_default():
    history = {'visible': [['q', 'a']], 'internal': [['q', 'a']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot')
    assert result['last_message_only'] is False


def test_chat_html_wrapper_last_message_only_true():
    history = {'visible': [['q', 'a']], 'internal': [['q', 'a']]}
    result = chat_html_wrapper(history, 'User', 'Bot', 'instruct', 'default', 'Bot',
                               last_message_only=True)
    assert result['last_message_only'] is True
