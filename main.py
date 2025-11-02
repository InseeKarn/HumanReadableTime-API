from fastapi import FastAPI
from datetime import datetime, timezone
import humanize

app = FastAPI()

@app.get("/readable")
async def readable_time(from_time: str, to_time: str = None):
    now = datetime.now(timezone.utc)
    from_dt = datetime.fromisoformat(from_time.replace("Z", "+00.00"))
    to_dt = datetime.fromisoformat(to_time.replace("Z", "+00.00")) if to_time else now

    delta = to_dt - from_dt
    return {"readable": humanize.precisedelta(delta)}