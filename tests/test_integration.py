"""Integration tests: verify that the service and repository work together."""


class TestIntegrationOrderService:
    def test_integration_successful_order(self, order_service):
        result = order_service.place_order("SHIRT", 2)

        assert result["success"] is True
        assert result["item"] == "T-Shirt"
        assert result["quantity"] == 2
        # 2 shirts * 25.00 = 50.00; including 20% tax = 60.00.
        assert result["total"] == 60.0

    def test_integration_stock_is_reduced_after_order(self, order_service):
        order_service.place_order("MUG", 3)
        product = order_service.repo.get_product("MUG")

        assert product["stock"] == 97

    def test_integration_unknown_product(self, order_service):
        result = order_service.place_order("PANTS", 1)

        assert result == {
            "success": False,
            "error": "Product not found",
        }

    def test_integration_order_exceeds_stock(self, order_service):
        result = order_service.place_order("HAT", 999)

        assert result == {
            "success": False,
            "error": "Not enough stock",
        }

    def test_integration_multiple_orders_deplete_stock(self, order_service):
        order_service.place_order("HAT", 10)
        order_service.place_order("HAT", 15)

        product = order_service.repo.get_product("HAT")
        assert product["stock"] == 5
