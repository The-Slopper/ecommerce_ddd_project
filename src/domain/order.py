"""
Order aggregate — core domain model for the Orders bounded context.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


@dataclass
class ShippingAddress:
    street: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass
class Order:
    """
    Order aggregate root.

    Encapsulates all order-related business rules and enforces invariants
    through its methods. External code must go through the aggregate to
    modify state.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str = ""
    items: List[OrderItem] = field(default_factory=list)
    shipping_address: Optional[ShippingAddress] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""

    def add_item(self, product_id: str, name: str, quantity: int, price: float) -> None:
        self.items.append(OrderItem(product_id, name, quantity, price))
        self.updated_at = datetime.utcnow()

    def remove_item(self, product_id: str) -> None:
        self.items = [i for i in self.items if i.product_id != product_id]
        self.updated_at = datetime.utcnow()

    def total(self) -> float:
        return sum(i.quantity * i.unit_price for i in self.items)

    def confirm(self) -> None:
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.utcnow()

    def ship(self) -> None:
        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.utcnow()

    def cancel(self) -> None:
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.utcnow()
