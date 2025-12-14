from __future__ import annotations

import os
import socket
from datetime import datetime, date
from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from fastapi import Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import Session

from models.user import UserCreate, UserRead, UserUpdate
from models.matcha_session import MatchaSessionCreate, MatchaSessionRead, MatchaSessionUpdate
from models.health import Health
from models.db_models import UserDB, MatchaSessionDB
from utils.database import get_db, init_db

port = int(os.environ.get("FASTAPIPORT", 8000))
port = int(os.environ.get("PORT", port))  # Cloud Run uses PORT

app = FastAPI(
    title="Matcha Drinking Tracker API",
    description="User service for tracking matcha drinking sessions and user profiles",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # You can replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    try:
        init_db()
    except Exception as e:
        # Log error but don't fail startup - tables might already exist
        print(f"Database initialization note: {e}")


# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )


@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)


@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# -----------------------------------------------------------------------------
# Helper functions for model conversion
# -----------------------------------------------------------------------------

def db_session_to_read(db_session: MatchaSessionDB) -> MatchaSessionRead:
    """Convert MatchaSessionDB to MatchaSessionRead."""
    return MatchaSessionRead(
        id=UUID(db_session.id),
        session_date=db_session.session_date,
        location=db_session.location,
        matcha_type=db_session.matcha_type,
        brand=db_session.brand,
        rating=db_session.rating,
        notes=db_session.notes,
        created_at=db_session.created_at,
        updated_at=db_session.updated_at,
    )


def db_user_to_read(db_user: UserDB) -> UserRead:
    """Convert UserDB to UserRead."""
    return UserRead(
        id=UUID(db_user.id),
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        phone=db_user.phone,
        favorite_matcha_powder=db_user.favorite_matcha_powder,
        favorite_matcha_place=db_user.favorite_matcha_place,
        matcha_budget=db_user.matcha_budget,
        join_date=db_user.join_date,
        matcha_sessions=[db_session_to_read(s) for s in db_user.matcha_sessions],
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


# -----------------------------------------------------------------------------
# Matcha Session endpoints
# -----------------------------------------------------------------------------

@app.post("/matcha-sessions", response_model=MatchaSessionRead, status_code=201)
def create_matcha_session(session: MatchaSessionCreate, db: Session = Depends(get_db)):
    # Check if session with this ID already exists
    existing = db.query(MatchaSessionDB).filter(MatchaSessionDB.id == str(session.id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Matcha session with this ID already exists")
    
    db_session = MatchaSessionDB(
        id=str(session.id),
        session_date=session.session_date,
        location=session.location,
        matcha_type=session.matcha_type,
        brand=session.brand,
        rating=session.rating,
        notes=session.notes,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session_to_read(db_session)


@app.get("/matcha-sessions", response_model=List[MatchaSessionRead])
def list_matcha_sessions(
    session_date: Optional[str] = Query(None, description="Filter by session date (YYYY-MM-DD)"),
    location: Optional[str] = Query(None, description="Filter by location"),
    matcha_type: Optional[str] = Query(None, description="Filter by matcha type"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    min_rating: Optional[float] = Query(None, description="Filter by minimum rating (0.0-5.0)"),
    max_rating: Optional[float] = Query(None, description="Filter by maximum rating (0.0-5.0)"),
    db: Session = Depends(get_db),
):
    query = db.query(MatchaSessionDB)
    
    if session_date is not None:
        query = query.filter(MatchaSessionDB.session_date == date.fromisoformat(session_date))
    if location is not None:
        query = query.filter(MatchaSessionDB.location == location)
    if matcha_type is not None:
        query = query.filter(MatchaSessionDB.matcha_type == matcha_type)
    if brand is not None:
        query = query.filter(MatchaSessionDB.brand == brand)
    if min_rating is not None:
        query = query.filter(MatchaSessionDB.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(MatchaSessionDB.rating <= max_rating)
    
    results = query.all()
    return [db_session_to_read(s) for s in results]


@app.get("/matcha-sessions/{session_id}", response_model=MatchaSessionRead)
def get_matcha_session(session_id: UUID, db: Session = Depends(get_db)):
    db_session = db.query(MatchaSessionDB).filter(MatchaSessionDB.id == str(session_id)).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    return db_session_to_read(db_session)


@app.put("/matcha-sessions/{session_id}", response_model=MatchaSessionRead)
def update_matcha_session(session_id: UUID, update: MatchaSessionUpdate, db: Session = Depends(get_db)):
    db_session = db.query(MatchaSessionDB).filter(MatchaSessionDB.id == str(session_id)).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_session, field, value)
    
    db_session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_session)
    return db_session_to_read(db_session)


@app.delete("/matcha-sessions/{session_id}", status_code=204)
def delete_matcha_session(session_id: UUID, db: Session = Depends(get_db)):
    db_session = db.query(MatchaSessionDB).filter(MatchaSessionDB.id == str(session_id)).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    db.delete(db_session)
    db.commit()
    return None


# -----------------------------------------------------------------------------
# User endpoints
# -----------------------------------------------------------------------------

@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_username = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    db_user = UserDB(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        favorite_matcha_powder=user.favorite_matcha_powder,
        favorite_matcha_place=user.favorite_matcha_place,
        matcha_budget=user.matcha_budget,
        join_date=user.join_date,
    )
    db.add(db_user)
    db.flush()  # Get the user ID
    
    # Create matcha sessions if provided
    if user.matcha_sessions:
        for session in user.matcha_sessions:
            db_session = MatchaSessionDB(
                id=str(session.id),
                user_id=db_user.id,
                session_date=session.session_date,
                location=session.location,
                matcha_type=session.matcha_type,
                brand=session.brand,
                rating=session.rating,
                notes=session.notes,
            )
            db.add(db_session)
    
    db.commit()
    db.refresh(db_user)
    return db_user_to_read(db_user)


@app.get("/users", response_model=List[UserRead])
def list_users(
    username: Optional[str] = Query(None, description="Filter by username"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    favorite_matcha_powder: Optional[str] = Query(None, description="Filter by favorite matcha powder"),
    favorite_matcha_place: Optional[str] = Query(None, description="Filter by favorite matcha place"),
    min_budget: Optional[float] = Query(None, description="Filter by minimum matcha budget"),
    max_budget: Optional[float] = Query(None, description="Filter by maximum matcha budget"),
    join_date: Optional[str] = Query(None, description="Filter by join date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    query = db.query(UserDB)
    
    if username is not None:
        query = query.filter(UserDB.username == username)
    if first_name is not None:
        query = query.filter(UserDB.first_name == first_name)
    if last_name is not None:
        query = query.filter(UserDB.last_name == last_name)
    if email is not None:
        query = query.filter(UserDB.email == email)
    if phone is not None:
        query = query.filter(UserDB.phone == phone)
    if favorite_matcha_powder is not None:
        query = query.filter(UserDB.favorite_matcha_powder == favorite_matcha_powder)
    if favorite_matcha_place is not None:
        query = query.filter(UserDB.favorite_matcha_place == favorite_matcha_place)
    if min_budget is not None:
        query = query.filter(UserDB.matcha_budget >= min_budget)
    if max_budget is not None:
        query = query.filter(UserDB.matcha_budget <= max_budget)
    if join_date is not None:
        query = query.filter(UserDB.join_date == date.fromisoformat(join_date))
    
    results = query.all()
    return [db_user_to_read(u) for u in results]


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user_to_read(db_user)


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = update.model_dump(exclude_unset=True)
    
    # Check for unique constraints if updating username or email
    if "username" in update_data and update_data["username"] != db_user.username:
        existing = db.query(UserDB).filter(UserDB.username == update_data["username"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    if "email" in update_data and update_data["email"] != db_user.email:
        existing = db.query(UserDB).filter(UserDB.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Handle matcha_sessions separately if provided
    if "matcha_sessions" in update_data:
        # Delete existing sessions
        db.query(MatchaSessionDB).filter(MatchaSessionDB.user_id == str(user_id)).delete()
        # Create new sessions
        for session in update_data["matcha_sessions"]:
            db_session = MatchaSessionDB(
                id=str(session.id),
                user_id=str(user_id),
                session_date=session.session_date,
                location=session.location,
                matcha_type=session.matcha_type,
                brand=session.brand,
                rating=session.rating,
                notes=session.notes,
            )
            db.add(db_session)
        del update_data["matcha_sessions"]
    
    # Update other fields
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user_to_read(db_user)


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)  # Cascade will delete related sessions
    db.commit()
    return None


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Matcha Drinking Tracker API. See /docs for OpenAPI UI."}


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
