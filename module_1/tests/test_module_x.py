"""Unit tests for module_x.py."""

import pytest

from module_x import (
    calculate_discount,
    classify_priority,
    is_valid_project_code,
    normalize_name,
    summarize_order,
)


class TestNormalizeName:
    def test_title_cases_simple_name(self):
        assert normalize_name("john smith") == "John Smith"

    def test_collapses_internal_whitespace(self):
        assert normalize_name("john    smith") == "John Smith"

    def test_strips_leading_and_trailing_whitespace(self):
        assert normalize_name("  john smith  ") == "John Smith"

    def test_handles_tabs_and_newlines(self):
        assert normalize_name("\tjohn\nsmith\t") == "John Smith"

    def test_already_title_cased(self):
        assert normalize_name("John Smith") == "John Smith"

    def test_single_word(self):
        assert normalize_name("john") == "John"

    def test_raises_type_error_for_non_string(self):
        with pytest.raises(TypeError):
            normalize_name(123)

    def test_raises_type_error_for_none(self):
        with pytest.raises(TypeError):
            normalize_name(None)

    def test_raises_value_error_for_empty_string(self):
        with pytest.raises(ValueError):
            normalize_name("")

    def test_raises_value_error_for_whitespace_only(self):
        with pytest.raises(ValueError):
            normalize_name("   ")
