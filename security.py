"""Security features for the FastAPI application."""
import os

import dotenv
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from starlette.exceptions import HTTPException

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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authentication credentials.')
