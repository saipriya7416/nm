from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MenuCategory, MenuItem
from ..schemas import MenuCategoryOut, MenuItemOut, MenuItemCreate

router = APIRouter()

@router.get("/categories", response_model=List[MenuCategoryOut])
def get_categories(db: Session = Depends(get_db)):
    """Fetch all menu categories."""
    return db.query(MenuCategory).all()

@router.get("/items", response_model=List[MenuItemOut])
def get_menu_items(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    is_vegetarian: Optional[bool] = Query(None, description="Filter for vegetarian items only"),
    search: Optional[str] = Query(None, description="Search term for dish name or description"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    """Fetch menu items with optional category, dietary, search, and price filters."""
    query = db.query(MenuItem).filter(MenuItem.availability == True)

    if category_id:
        query = query.filter(MenuItem.category_id == category_id)

    if is_vegetarian is not None:
        query = query.filter(MenuItem.is_vegetarian == is_vegetarian)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter((MenuItem.name.ilike(term)) | (MenuItem.description.ilike(term)) | (MenuItem.ingredients.ilike(term)))

    if min_price is not None:
        query = query.filter(MenuItem.price >= min_price)

    if max_price is not None:
        query = query.filter(MenuItem.price <= max_price)

    items = query.all()
    # Map category names
    result = []
    for item in items:
        out = MenuItemOut.model_validate(item)
        if item.category:
            out.category_name = item.category.name
        result.append(out)
    return result

@router.get("/items/{item_id}", response_model=MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Fetch a single menu item by ID."""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    out = MenuItemOut.model_validate(item)
    if item.category:
        out.category_name = item.category.name
    return out

@router.post("/items", response_model=MenuItemOut)
def create_menu_item(item_in: MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item (Admin endpoint)."""
    item = MenuItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    out = MenuItemOut.model_validate(item)
    if item.category:
        out.category_name = item.category.name
    return out
