import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from storeapi.controller.controller import router as api_router
from storeapi.controller.user import router as user_router
from storeapi.db.database import database
from storeapi.logging_config import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler to connect and disconnect the database.
    """
    configure_logging()  # Configure logging at the start
    logger.info("Starting application lifespan")
    logger.debug("Connecting to the database")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(api_router, prefix="/posts", tags=["posts"])
app.include_router(user_router, prefix="/users", tags=["users"])

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(CorrelationIdMiddleware)


@app.get("/")
async def root():
    return {"message": "Welcome to the Store API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(req, exc):
    logger.error(f"Status: {exc.status_code} HTTP Exception: {exc.detail}")
    return await http_exception_handler(req, exc)
