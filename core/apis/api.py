from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database.database import connect_to_mongo, close_mongo_connection
from core.routers.user_router import router as user_router
from core import logger

logging = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Starting User Management API")
        await connect_to_mongo()
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
    yield
    logging.info("Shutting down User Management API")
    await close_mongo_connection()


app = FastAPI(
    title="User Management API",
    description="API for user management",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(user_router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Welcome to the User Management API!"}
