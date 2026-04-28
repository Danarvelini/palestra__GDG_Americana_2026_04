from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Literal

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
    users_db[user_id]["active"] = False

    audit_log.append(
        {
            "action": "delete",
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    return None
