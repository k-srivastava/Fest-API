"""Security features for the FastAPI application."""
import os
import secrets

import dotenv
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.exceptions import HTTPException

from math import sqrt

_security = HTTPBearer()

dotenv.load_dotenv()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(_security)):
    """
    Verify whether the bearer token is valid by comparing against a defined token.

    :param credentials: HTTP credentials that contain the bearer token.
    :type credentials: HTTPAuthorizationCredentials

    :raise HTTPException: The bearer token is invalid.
    """
    token = credentials.credentials
    expected_token = os.getenv('BEARER_TOKEN')

    if token != expected_token:
        raise HTTPException(status_code=403, detail='Invalid authentication credentials.')


def to_base36(num: int) -> str:
    """
    Converts a base-10 number to a base-36 string.

    :param num: The base-10 number (integer).
    :return: The base-36 representation as a string.
    """
    if num < 0:
        raise ValueError("Only non-negative numbers are supported.")

    if num == 0:
        return "0"

    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36_str = ""

    # Convert base-10 to base-36
    while num:
        base36_str = chars[num % 36] + base36_str
        num //= 36

    return base36_str

def from_base36(base36_str: str) -> int:
    """
    Converts a base-36 string to a base-10 integer.

    :param base36_str: The base-36 number as a string.
    :return: The base-10 integer representation.
    """
    return int(base36_str, 36)


def generate_user_id(length: int) -> str:
    key_check = int(os.getenv('ID_GEN_KEY'))
    if key_check >= sqrt(36**length):
        raise ValueError(f'Key is too big for given length! Key must be smaller than {sqrt(36**length)}')

    pool = "0123456789abcdefghijklmnopqrstuvwxyz"
    h = "".join(secrets.choice(pool) for _ in range(length))

    num = from_base36(h)
    n2 = num + (-num % key_check)  # Ensures num is a multiple of key_check
    code = to_base36(n2)
    if len(code) == length:
        return code
    else:
        n2 = num - (num % key_check)
        return to_base36(n2)


def validate_user_id(user_id: str) -> bool:
    key = int(os.getenv('ID_GEN_KEY'))
    return from_base36(user_id) % key == 0