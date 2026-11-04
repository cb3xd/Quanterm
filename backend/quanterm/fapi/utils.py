import re

from fastapi import HTTPException

_search = re.compile(r"^[a-z0-9-]+$").search


def validate_symbol(symbol: str):
    if not bool(_search(symbol)):
        raise HTTPException(422, "Invalid symbol format.")
