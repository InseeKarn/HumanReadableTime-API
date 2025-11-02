# seed.py
from database import User, SessionLocal

def Default_db():
    db = SessionLocal()

    # Free user
    if not db.query(User).filter(User.api_key == "free-api-key").first():
        free_user = User(
            api_key="free-api-key",
            plan="Free",
            usage=0,
            quota=50
        )
        db.add(free_user)

    # Paid user
    if not db.query(User).filter(User.api_key == "paid-api-key").first():
        paid_user = User(
            api_key="paid-api-key",
            plan="Premium",
            usage=0,
            quota=100
        )
        db.add(paid_user)

    db.commit()
    print("Default users added")
    db.close()
