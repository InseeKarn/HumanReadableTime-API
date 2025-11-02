# endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from dateutil import parser
from database import User
import humanize
from auth import get_api_user

router = APIRouter()

@router.get("/readable")
async def readable_time(
    from_time: str,
    to_time: str = None,
    relative: bool = False,
    api_data: tuple = Depends(get_api_user)
):
    api_user, db = api_data
    now = datetime.now(timezone.utc)


    if api_user.plan == "Free" and relative:
        if relative:
            raise HTTPException(status_code=403, detail="Upgrade to premium to use 'relative=true'")

    # parse from_time
    try:
        from_dt = parser.parse(from_time)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid from_time format")

    # parse to_time
    if to_time:
        try:
            to_dt = parser.parse(to_time)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid to_time format")
    else:
        to_dt = now

    delta = to_dt - from_dt

    if relative:
        result = humanize.naturaltime(delta)
    else:
        result = humanize.precisedelta(delta)
        
    db.close()
    return {"readable": result}
