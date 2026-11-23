"""Unit tests: each test checks one function in isolation."""
import pytest

from app import calculate_discount, calculate_tax, calculate_total


class TestCalculateDiscount:
    def test_unit_10_percent_off(self):
        assert calculate_discount(100, 10) == 90.0

    def test_unit_zero_discount_keeps_full_price(self):
        assert calculate_discount(50, 0) == 50.0

    def test_unit_100_percent_discount_is_free(self):
        assert calculate_discount(75, 100) == 0.0

    def test_unit_handles_decimals(self):
        assert calculate_discount(19.99, 15) == 16.99

    def test_unit_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10, 20)

    @pytest.mark.parametrize("discount", [-1, 101])
    def test_unit_invalid_discount_raises_error(self, discount):
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100, discount)


class TestCalculateTax:
    def test_unit_default_20_percent_tax(self):
        assert calculate_tax(100) == 20.0

    def test_unit_custom_tax_rate(self):
        assert calculate_tax(100, 0.10) == 10.0

    def test_unit_zero_price_has_zero_tax(self):
        assert calculate_tax(0) == 0.0


class TestCalculateTotal:
    def test_unit_single_item_total(self):
        assert calculate_total([50.0]) == 60.0

    def test_unit_multiple_items_total(self):
        assert calculate_total([10.0, 20.0, 30.0]) == 72.0

    def test_unit_empty_cart(self):
        assert calculate_total([]) == 0.0

    def test_unit_custom_tax_rate(self):
        assert calculate_total([100.0], tax_rate=0.10) == 110.0
