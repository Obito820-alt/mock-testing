"""Shared pytest fixtures."""
import pytest

from app import OrderService, ProductRepository


@pytest.fixture
def order_service():
    """Provide a fresh repository and service for each integration test."""
    repository = ProductRepository()
    return OrderService(repository)
