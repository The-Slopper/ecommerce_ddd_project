"""
Tests for the Orders bounded context.
"""

import pytest
from unittest.mock import MagicMock
from src.application.order_service import OrderService
from src.infrastructure.order_repository import OrderModel


def make_session():
    session = MagicMock()
    return session


def test_create_order_returns_model():
    session = make_session()
    session.get.return_value = None
    svc = OrderService(session)
    order = svc.create_order(
        "user-1",
        [{"quantity": 2, "unit_price": 10.0, "product_id": "p1", "name": "Widget"}],
    )
    assert order.customer_id == "user-1"
    assert order.total == 20.0


def test_cancel_order_not_found():
    session = make_session()
    session.get.return_value = None
    svc = OrderService(session)
    result = svc.cancel_order("nonexistent", "user-1")
    assert result is False


def test_cancel_order_success():
    session = make_session()
    mock_order = MagicMock()
    mock_order.status = "pending"
    session.get.return_value = mock_order
    svc = OrderService(session)
    svc.cancel_order("order-1", "user-1")


def test_list_customer_orders():
    session = make_session()
    session.query.return_value.filter_by.return_value.order_by.return_value.all.return_value = []
    svc = OrderService(session)
    result = svc.list_customer_orders("user-1")
    assert result == []
