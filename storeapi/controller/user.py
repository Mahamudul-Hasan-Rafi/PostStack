import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from storeapi.db.database import database, user_table
from storeapi.models.models import User
from storeapi.security.security import (
    authenticate_user,
    create_access_token,
    get_user,
    hash_password,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register")
async def register_user(user: User):
    # Simulate user registration
    new_user = user.model_dump()

    existing_user = await get_user(new_user["username"])
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    # In a real application, you would save this to a database
    logger.info(f"Registering user: {new_user['username']}")
    query = user_table.insert().values(
        username=new_user["username"],
        email=new_user["email"],
        hashed_password=await hash_password(
            new_user["password"]
        ),  # Note: Password should be hashed in production
    )

    logger.debug(f"Executing query: {query}")

    await database.execute(query)

    return JSONResponse(
        content="User Created Successfully", status_code=status.HTTP_201_CREATED
    )


@router.get("/login")
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a real application, you would generate a JWT token here
    return JSONResponse(
        content={
            "access_token": await create_access_token(
                {
                    "id": user["id"],
                    "sub": user["username"],
                    "email": user["email"],
                },
                expires_delta=15,  # Token valid for 1 hour
            ),
            "token_type": "bearer",
        }
    )
