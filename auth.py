# auth.py
from fastapi import HTTPException, Header, Depends
from database import User, SessionLocal

def get_api_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    api_key = authorization.split(" ")[1]

    db = SessionLocal()
    user = db.query(User).filter(User.api_key == api_key).first()

    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user.plan == "Free" and user.usage >= user.quota:
        db.close()
        raise HTTPException(status_code=429, detail="Quota exceeded, upgrade to premium")
    
    if user.plan == "Free":
        user.usage += 1
        db.commit()
    

    return user, db
