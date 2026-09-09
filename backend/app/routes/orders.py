from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, OrderItem, MenuItem
from ..schemas import OrderCreate, OrderOut, OrderItemOut

router = APIRouter()

@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    """Create a new food order."""
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    total = 0.0
    order_items_to_add = []

    for item_in in payload.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item_in.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item #{item_in.menu_item_id} not found")
        item_total = menu_item.price * item_in.quantity
        total += item_total
        order_items_to_add.append(
            OrderItem(
                menu_item_id=menu_item.id,
                quantity=item_in.quantity,
                price=menu_item.price
            )
        )

    new_order = Order(
        customer_name=payload.customer_name or "Guest",
        customer_phone=payload.customer_phone or "+1 555-0199",
        order_type=payload.order_type,
        table_number=payload.table_number,
        total_amount=round(total, 2),
        status="Order Placed",
        payment_method=payload.payment_method,
        payment_status="Paid",
        special_instructions=payload.special_instructions,
        user_id=payload.user_id,
        items=order_items_to_add
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Format output
    out = OrderOut.model_validate(new_order)
    out.items = [
        OrderItemOut(
            id=oi.id,
            menu_item_id=oi.menu_item_id,
            name=oi.menu_item.name if oi.menu_item else "Item",
            quantity=oi.quantity,
            price=oi.price
        )
        for oi in new_order.items
    ]
    return out

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Look up order by reference ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found")
    
    out = OrderOut.model_validate(order)
    out.items = [
        OrderItemOut(
            id=oi.id,
            menu_item_id=oi.menu_item_id,
            name=oi.menu_item.name if oi.menu_item else "Item",
            quantity=oi.quantity,
            price=oi.price
        )
        for oi in order.items
    ]
    return out

@router.get("", response_model=List[OrderOut])
def list_orders(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """List recent orders."""
    query = db.query(Order).order_by(Order.created_at.desc())
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    orders = query.limit(20).all()
    result = []
    for o in orders:
        out = OrderOut.model_validate(o)
        out.items = [
            OrderItemOut(
                id=oi.id,
                menu_item_id=oi.menu_item_id,
                name=oi.menu_item.name if oi.menu_item else "Item",
                quantity=oi.quantity,
                price=oi.price
            )
            for oi in o.items
        ]
        result.append(out)
    return result

@router.post("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    """Update status of an active order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    
    out = OrderOut.model_validate(order)
    out.items = [
        OrderItemOut(
            id=oi.id,
            menu_item_id=oi.menu_item_id,
            name=oi.menu_item.name if oi.menu_item else "Item",
            quantity=oi.quantity,
            price=oi.price
        )
        for oi in order.items
    ]
    return out
