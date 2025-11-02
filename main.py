# main.py
from fastapi import FastAPI
from endpoints import router as readable_router
from seed import Default_db

app = FastAPI(title="Human Readable Time API")

@app.on_event("startup")
def startup_event():
    Default_db()

app.include_router(readable_router)
