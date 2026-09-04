import re

from fastapi import HTTPException


def validate_symbol(symbol, search=re.compile(r"^[a-z0-9-]+$").search):
    if not bool(search(symbol)):
        print(bool(search(symbol)))
        raise HTTPException(422, "Invalid symbol format.")
