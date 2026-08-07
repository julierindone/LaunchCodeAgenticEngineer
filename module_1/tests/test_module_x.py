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


class TestSummarizeOrder:
    def test_empty_order(self):
        assert summarize_order([]) == {"item_count": 0, "subtotal": 0.0}

    def test_single_item(self):
        result = summarize_order([{"quantity": 2, "unit_price": 5.0}])
        assert result == {"item_count": 2, "subtotal": 10.0}

    def test_multiple_items(self):
        items = [
            {"quantity": 2, "unit_price": 5.0},
            {"quantity": 1, "unit_price": 3.5},
        ]
        result = summarize_order(items)
        assert result == {"item_count": 3, "subtotal": 13.5}

    def test_rounds_subtotal_to_two_decimal_places(self):
        items = [{"quantity": 3, "unit_price": 0.1}]
        result = summarize_order(items)
        assert result == {"item_count": 3, "subtotal": 0.3}

    def test_missing_quantity_defaults_to_zero(self):
        result = summarize_order([{"unit_price": 5.0}])
        assert result == {"item_count": 0, "subtotal": 0.0}

    def test_missing_unit_price_defaults_to_zero(self):
        result = summarize_order([{"quantity": 2}])
        assert result == {"item_count": 2, "subtotal": 0.0}

    def test_accepts_int_unit_price(self):
        result = summarize_order([{"quantity": 2, "unit_price": 5}])
        assert result == {"item_count": 2, "subtotal": 10.0}

    def test_zero_quantity_item(self):
        result = summarize_order([{"quantity": 0, "unit_price": 5.0}])
        assert result == {"item_count": 0, "subtotal": 0.0}

    def test_raises_value_error_for_negative_quantity(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": -1, "unit_price": 5.0}])

    def test_raises_value_error_for_non_int_quantity(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 2.5, "unit_price": 5.0}])

    def test_raises_value_error_for_negative_unit_price(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 1, "unit_price": -5.0}])

    def test_raises_value_error_for_non_numeric_unit_price(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 1, "unit_price": "5.0"}])


class TestIsValidProjectCode:
    def test_valid_code(self):
        assert is_valid_project_code("AB-1234") is True

    def test_invalid_lowercase_prefix(self):
        assert is_valid_project_code("ab-1234") is False

    def test_invalid_mixed_case_prefix(self):
        assert is_valid_project_code("Ab-1234") is False

    def test_invalid_prefix_length(self):
        assert is_valid_project_code("ABC-1234") is False

    def test_invalid_prefix_non_alpha(self):
        assert is_valid_project_code("A1-1234") is False

    def test_invalid_number_length(self):
        assert is_valid_project_code("AB-123") is False
        assert is_valid_project_code("AB-12345") is False

    def test_invalid_number_non_digit(self):
        assert is_valid_project_code("AB-12A4") is False

    def test_missing_separator(self):
        assert is_valid_project_code("AB1234") is False

    def test_too_many_separators(self):
        assert is_valid_project_code("AB-12-34") is False

    def test_non_string_input_returns_false(self):
        assert is_valid_project_code(1234) is False

    def test_none_input_returns_false(self):
        assert is_valid_project_code(None) is False

    def test_empty_string_returns_false(self):
        assert is_valid_project_code("") is False
