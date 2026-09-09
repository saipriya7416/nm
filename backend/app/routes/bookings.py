from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking, RestaurantTable
from ..schemas import BookingCreate, BookingOut, RestaurantTableOut

router = APIRouter()

@router.get("/tables", response_model=List[RestaurantTableOut])
def get_tables(db: Session = Depends(get_db)):
    """Fetch all restaurant tables and their current status."""
    return db.query(RestaurantTable).all()

@router.post("", response_model=BookingOut)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """Reserve a table in the restaurant."""
    # Find suitable table
    table_query = db.query(RestaurantTable).filter(RestaurantTable.capacity >= payload.number_of_people)
    if payload.table_preference and payload.table_preference != "Any":
        table_query = table_query.filter(RestaurantTable.location.ilike(f"%{payload.table_preference}%"))
    
    assigned_table = table_query.first()
    if not assigned_table:
        assigned_table = db.query(RestaurantTable).filter(RestaurantTable.capacity >= payload.number_of_people).first()
    if not assigned_table:
        assigned_table = db.query(RestaurantTable).first()

    new_booking = Booking(
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone or "+1 555-0199",
        customer_email=payload.customer_email or "guest@example.com",
        date=payload.date,
        time=payload.time,
        number_of_people=payload.number_of_people,
        table_preference=payload.table_preference or (assigned_table.location if assigned_table else "Main Dining Hall"),
        special_requests=payload.special_requests,
        table_id=assigned_table.id if assigned_table else 1,
        user_id=payload.user_id,
        status="Confirmed"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Look up a booking by reference ID."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking #{booking_id} not found")
    return booking

@router.get("", response_model=List[BookingOut])
def list_bookings(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """List bookings with optional user filter."""
    query = db.query(Booking).order_by(Booking.created_at.desc())
    if user_id:
        query = query.filter(Booking.user_id == user_id)
    return query.limit(20).all()

@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel an active booking."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "Cancelled"
    db.commit()
    db.refresh(booking)
    return booking
