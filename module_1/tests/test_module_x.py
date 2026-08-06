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


class TestCalculateDiscount:
    def test_standard_tier_no_discount(self):
        assert calculate_discount(100.0, "standard") == 100.0

    def test_silver_tier_discount(self):
        assert calculate_discount(100.0, "silver") == 95.0

    def test_gold_tier_discount(self):
        assert calculate_discount(100.0, "gold") == 90.0

    def test_platinum_tier_discount(self):
        assert calculate_discount(100.0, "platinum") == 85.0

    def test_tier_is_case_insensitive(self):
        assert calculate_discount(100.0, "GOLD") == 90.0

    def test_tier_strips_whitespace(self):
        assert calculate_discount(100.0, "  gold  ") == 90.0

    def test_rounds_to_two_decimal_places(self):
        assert calculate_discount(10.0, "silver") == 9.5
        assert calculate_discount(10.003, "standard") == 10.0

    def test_zero_price(self):
        assert calculate_discount(0.0, "gold") == 0.0

    def test_raises_value_error_for_negative_price(self):
        with pytest.raises(ValueError):
            calculate_discount(-1.0, "gold")

    def test_raises_value_error_for_unknown_tier(self):
        with pytest.raises(ValueError):
            calculate_discount(100.0, "bronze")

    def test_raises_value_error_for_empty_tier(self):
        with pytest.raises(ValueError):
            calculate_discount(100.0, "")


class TestClassifyPriority:
    def test_urgent_boundary(self):
        assert classify_priority(90) == "urgent"

    def test_urgent_max(self):
        assert classify_priority(100) == "urgent"

    def test_high_boundary(self):
        assert classify_priority(70) == "high"

    def test_high_upper_edge(self):
        assert classify_priority(89) == "high"

    def test_medium_boundary(self):
        assert classify_priority(40) == "medium"

    def test_medium_upper_edge(self):
        assert classify_priority(69) == "medium"

    def test_low_boundary(self):
        assert classify_priority(0) == "low"

    def test_low_upper_edge(self):
        assert classify_priority(39) == "low"

    def test_raises_type_error_for_non_int(self):
        with pytest.raises(TypeError):
            classify_priority(50.5)

    def test_raises_type_error_for_bool_is_allowed_as_int(self):
        # bool is a subclass of int in Python, so this should not raise TypeError.
        assert classify_priority(True) == "low"

    def test_raises_type_error_for_string(self):
        with pytest.raises(TypeError):
            classify_priority("50")

    def test_raises_value_error_for_negative_score(self):
        with pytest.raises(ValueError):
            classify_priority(-1)

    def test_raises_value_error_for_score_above_100(self):
        with pytest.raises(ValueError):
            classify_priority(101)
