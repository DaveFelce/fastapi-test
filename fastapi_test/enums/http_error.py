from enum import Enum

from fastapi import HTTPException, status


class HttpErrors(Enum):
    INVALID_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "display_message": "Supplied token is invalid.",
            "code": "INVALID_TOKEN",
        },
    )
    NO_USER_FOUND = HTTPException(
        detail={
            "display_message": "User not found for provided name.",
            "code": "NO_USER_FOUND",
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )
    USER_EXISTS = HTTPException(
        detail={
            "display_message": "It appears this user already exists.",
            "code": "USER_EXISTS",
            "fields": ["username"],
        },
        status_code=status.HTTP_409_CONFLICT,
    )
