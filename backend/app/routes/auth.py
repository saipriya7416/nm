from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, UserOut, Token

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new customer account."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        hashed_password="mock_hashed_pw" # Lightweight mock hashing for demo
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """Login and obtain access token."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        # Create demo user on the fly if not exists
        user = User(
            name=payload.email.split("@")[0].capitalize(),
            email=payload.email,
            phone="+1 555-0199",
            hashed_password="demo_password"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return Token(
        access_token=f"demo_token_for_{user.id}",
        token_type="bearer",
        user=UserOut.model_validate(user)
    )

@router.get("/me", response_model=UserOut)
def get_current_user(db: Session = Depends(get_db)):
    """Get the active user profile."""
    user = db.query(User).first()
    if not user:
        user = User(name="Alex Morgan", email="alex@example.com", phone="+1 555-0199")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
