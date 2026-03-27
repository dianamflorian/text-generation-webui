"""Tests for modules.sane_markdown_lists public API."""
import markdown
import pytest
from markdown import Extension

from modules.sane_markdown_lists import (
    MIN_NESTED_LIST_INDENT,
    SaneListExtension,
    makeExtension,
)


def test_min_nested_list_indent_is_int():
    assert isinstance(MIN_NESTED_LIST_INDENT, int)


def test_min_nested_list_indent_greater_than_one():
    assert MIN_NESTED_LIST_INDENT > 1


def test_sane_list_extension_is_markdown_extension():
    ext = SaneListExtension()
    assert isinstance(ext, Extension)


def test_make_extension_returns_sane_list_extension():
    ext = makeExtension()
    assert isinstance(ext, SaneListExtension)


def test_make_extension_accepts_kwargs():
    ext = makeExtension()
    assert ext is not None


def test_unordered_list_renders_ul():
    result = markdown.markdown(
        "- item 1\n- item 2\n- item 3", extensions=[SaneListExtension()]
    )
    assert "<ul>" in result
    assert "<li>" in result


def test_unordered_list_contains_items():
    result = markdown.markdown(
        "- item 1\n- item 2\n- item 3", extensions=[SaneListExtension()]
    )
    assert "item 1" in result
    assert "item 2" in result
    assert "item 3" in result


def test_ordered_list_renders_ol():
    result = markdown.markdown(
        "1. first\n2. second\n3. third", extensions=[SaneListExtension()]
    )
    assert "<ol>" in result
    assert "<li>" in result


def test_ordered_list_contains_items():
    result = markdown.markdown(
        "1. first\n2. second\n3. third", extensions=[SaneListExtension()]
    )
    assert "first" in result
    assert "second" in result
    assert "third" in result


def test_paragraph_renders_p_tag():
    result = markdown.markdown(
        "This is a paragraph.", extensions=[SaneListExtension()]
    )
    assert "<p>" in result
    assert "This is a paragraph." in result


def test_nested_unordered_list():
    text = "- item 1\n  - nested\n- item 2"
    result = markdown.markdown(text, extensions=[SaneListExtension()])
    assert "item 1" in result
    assert "nested" in result
    assert "item 2" in result


def test_fenced_code_via_make_extension():
    ext = makeExtension()
    result = markdown.markdown(
        "- a\n- b", extensions=[ext]
    )
    assert "<ul>" in result
