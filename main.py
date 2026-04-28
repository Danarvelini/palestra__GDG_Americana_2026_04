from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin", "active": True},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "viewer", "active": True},
}

audit_log = []


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user or not user["active"]:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    user = users_db.get(user_id)
    if not user or not user["active"]:
        raise HTTPException(status_code=404, detail="User not found")
    audit_log.append(
        {
            "action": "delete",
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    return None


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    role: str = "admin"


@app.post("/users", status_code=201)
def create_user(payload: UserCreateRequest):
    new_id = len(users_db) + 1
    user = {
        "id": new_id,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "active": True,
    }
    users_db[new_id] = user
    return user
