import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from storeapi.db.database import database, user_table

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "MY-APP"
ALGORITHM = "HS256"

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def create_access_token(data: dict, expires_delta: int = None) -> str:
    """
    Create a JWT access token.
    :param data: The data to encode in the token.
    :param expires_delta: Optional expiration time in seconds.
    :return: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.now(UTC) + timedelta(minutes=15)})
    else:
        to_encode.update({"exp": datetime.now(UTC) + timedelta(minutes=15)})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    :param password: The plain text password to hash.
    :return: The hashed password.
    """
    return cryptContext.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return cryptContext.verify(plain_password, hashed_password)


async def get_user(username: str):
    """
    Mock function to simulate user retrieval.
    In a real application, this would query the database or an external service.
    """
    # Simulating a user retrieval

    query = user_table.select().where(user_table.c.username == username)

    logger.debug(f"Executing query to get user: {query}")

    result = await database.fetch_one(query)

    logger.debug(f"Querying user with username: {username}")
    logger.debug(f"Query result: {result}")

    if not result:
        return None

    return {
        "id": result["id"],
        "username": result["username"],
        "email": result["email"],
        "hashed_password": result["hashed_password"],
    }


async def authenticate_user(username: str, password: str):
    """
    Authenticate a user by username and password.
    :param username: The username of the user.
    :param password: The plain text password of the user.
    :return: The user data if authentication is successful, None otherwise.
    """
    user = await get_user(username)
    if not user or not await verify_password(password, user["hashed_password"]):
        return None

    return user


async def get_current_user(token: Annotated[str, Depends] = Depends(oauth2_scheme)):
    """
    Get the current user from the JWT token.
    :param token: The JWT token from the request.
    :return: The user data if the token is valid, raises HTTPException otherwise.
    """
    try:
        logger.debug(f"Received token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        logger.debug(f"Decoded JWT payload: {payload}")
        if username is None:
            raise credential_exception
        user = await get_user(username)
        logger.debug(f"Retrieved user: {user}")
        if user is None:
            raise credential_exception
        return user
    except jwt.JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credential_exception
