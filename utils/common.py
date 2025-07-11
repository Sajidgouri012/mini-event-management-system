"""
Common utilities for timezone conversion and rate limiting.
"""

import pytz
from datetime import datetime, timezone, timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

IST = pytz.timezone('Asia/Kolkata')

def ist_to_utc(ist_time: datetime) -> datetime:
    """
    Convert IST time to UTC time for DB storage.
    """
    if ist_time.tzinfo is None:
        ist_time = IST.localize(ist_time)
    return ist_time.astimezone(timezone.utc)

def get_ist_datetime(offset_hours: int):
    """
    Utility for testing: get current IST time with an offset.
    """
    return datetime.now(IST) + timedelta(hours=offset_hours)

limiter = Limiter(key_func=get_remote_address)
