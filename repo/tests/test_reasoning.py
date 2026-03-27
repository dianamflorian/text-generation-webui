"""Tests for modules.reasoning public API."""
import pytest
from modules.reasoning import extract_reasoning, THINKING_FORMATS


def test_thinking_formats_is_list():
    assert isinstance(THINKING_FORMATS, list)


def test_thinking_formats_nonempty():
    assert len(THINKING_FORMATS) > 0


def test_thinking_formats_entries_are_3tuples():
    for entry in THINKING_FORMATS:
        assert isinstance(entry, tuple)
        assert len(entry) == 3


def test_extract_reasoning_basic_think_tag():
    thinking, content = extract_reasoning("<think>I am thinking</think>The answer is 42")
    assert thinking == "I am thinking"
    assert content == "The answer is 42"


def test_extract_reasoning_no_thinking_block():
    thinking, content = extract_reasoning("Just a plain response")
    assert thinking is None
    assert content == "Just a plain response"


def test_extract_reasoning_empty_string():
    thinking, content = extract_reasoning("")
    assert thinking is None
    assert content == ""


def test_extract_reasoning_none_input():
    thinking, content = extract_reasoning(None)
    assert thinking is None
    assert content is None


def test_extract_reasoning_incomplete_think_tag_captures_rest():
    thinking, content = extract_reasoning("<think>Still thinking...")
    assert thinking == "Still thinking..."
    assert content == ""


def test_extract_reasoning_html_escaped_think_tag():
    thinking, content = extract_reasoning(
        "&lt;think&gt;thought&lt;/think&gt;answer", html_escaped=True
    )
    assert thinking == "thought"
    assert content == "answer"


def test_extract_reasoning_returns_tuple_of_two():
    result = extract_reasoning("some text")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_extract_reasoning_lstrips_content():
    # extract_reasoning uses lstrip() on the remaining content
    thinking, content = extract_reasoning("<think>thought</think>  answer")
    assert thinking == "thought"
    assert content == "answer"


def test_extract_reasoning_empty_think_tag():
    thinking, content = extract_reasoning("<think></think>after")
    assert thinking == ""
    assert content == "after"
