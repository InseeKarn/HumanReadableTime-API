from fastapi import APIRouter, HTTPException
from database import User, SessionLocal

router = APIRouter()

@router.post("/admin/add_user")
def add_user(api_key: str, plan: str = "Free", quota: int = 50):
    db = SessionLocal()

    existing = db.query(User).filter(User.api_key == api_key).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="API key already exists")
    
    new_user = User(api_key=api_key, plan=plan, usage=0, quota=quota)
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": f"User {api_key} added successfully", "plan": plan, "quota": quota}
