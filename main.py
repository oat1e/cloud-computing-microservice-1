from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.user import UserCreate, UserRead, UserUpdate
from models.matcha_session import MatchaSessionCreate, MatchaSessionRead, MatchaSessionUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
users: Dict[UUID, UserRead] = {}
matcha_sessions: Dict[UUID, MatchaSessionRead] = {}

app = FastAPI(
    title="Matcha Drinking Tracker API",
    description="User service for tracking matcha drinking sessions and user profiles",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
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
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Matcha Session endpoints
# -----------------------------------------------------------------------------

@app.post("/matcha-sessions", response_model=MatchaSessionRead, status_code=201)
def create_matcha_session(session: MatchaSessionCreate):
    if session.id in matcha_sessions:
        raise HTTPException(status_code=400, detail="Matcha session with this ID already exists")
    matcha_sessions[session.id] = MatchaSessionRead(**session.model_dump())
    return matcha_sessions[session.id]

@app.get("/matcha-sessions", response_model=List[MatchaSessionRead])
def list_matcha_sessions(
    session_date: Optional[str] = Query(None, description="Filter by session date (YYYY-MM-DD)"),
    location: Optional[str] = Query(None, description="Filter by location"),
    matcha_type: Optional[str] = Query(None, description="Filter by matcha type"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    min_rating: Optional[float] = Query(None, description="Filter by minimum rating (0.0-5.0)"),
    max_rating: Optional[float] = Query(None, description="Filter by maximum rating (0.0-5.0)"),
):
    results = list(matcha_sessions.values())

    if session_date is not None:
        results = [s for s in results if str(s.session_date) == session_date]
    if location is not None:
        results = [s for s in results if s.location == location]
    if matcha_type is not None:
        results = [s for s in results if s.matcha_type == matcha_type]
    if brand is not None:
        results = [s for s in results if s.brand == brand]
    if min_rating is not None:
        results = [s for s in results if s.rating is not None and s.rating >= min_rating]
    if max_rating is not None:
        results = [s for s in results if s.rating is not None and s.rating <= max_rating]

    return results

@app.get("/matcha-sessions/{session_id}", response_model=MatchaSessionRead)
def get_matcha_session(session_id: UUID):
    if session_id not in matcha_sessions:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    return matcha_sessions[session_id]

@app.put("/matcha-sessions/{session_id}", response_model=MatchaSessionRead)
def update_matcha_session(session_id: UUID, update: MatchaSessionUpdate):
    if session_id not in matcha_sessions:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    stored = matcha_sessions[session_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    matcha_sessions[session_id] = MatchaSessionRead(**stored)
    return matcha_sessions[session_id]

@app.delete("/matcha-sessions/{session_id}", status_code=204)
def delete_matcha_session(session_id: UUID):
    if session_id not in matcha_sessions:
        raise HTTPException(status_code=404, detail="Matcha session not found")
    del matcha_sessions[session_id]
    return None

# -----------------------------------------------------------------------------
# User endpoints
# -----------------------------------------------------------------------------

@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate):
    # Each user gets its own UUID; stored as UserRead
    user_read = UserRead(**user.model_dump())
    users[user_read.id] = user_read
    return user_read

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
):
    results = list(users.values())

    if username is not None:
        results = [u for u in results if u.username == username]
    if first_name is not None:
        results = [u for u in results if u.first_name == first_name]
    if last_name is not None:
        results = [u for u in results if u.last_name == last_name]
    if email is not None:
        results = [u for u in results if u.email == email]
    if phone is not None:
        results = [u for u in results if u.phone == phone]
    if favorite_matcha_powder is not None:
        results = [u for u in results if u.favorite_matcha_powder == favorite_matcha_powder]
    if favorite_matcha_place is not None:
        results = [u for u in results if u.favorite_matcha_place == favorite_matcha_place]
    if min_budget is not None:
        results = [u for u in results if u.matcha_budget is not None and u.matcha_budget >= min_budget]
    if max_budget is not None:
        results = [u for u in results if u.matcha_budget is not None and u.matcha_budget <= max_budget]
    if join_date is not None:
        results = [u for u in results if str(u.join_date) == join_date]

    return results

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, update: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    stored = users[user_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    users[user_id] = UserRead(**stored)
    return users[user_id]

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
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