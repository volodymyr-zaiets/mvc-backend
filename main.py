from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import init_db
from controllers.user_controller import router as user_router
from controllers.post_controller import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the FastAPI application's lifespan.

    This function is executed when the application starts and stops.
    It is typically used to initialize resources like database connections, caches, etc.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    init_db()  # Initialize the database (create tables, connect, etc.)
    print("Таблиці створено.")  # Optional: log to console when DB tables are created
    yield


# Instantiate the FastAPI application
app = FastAPI(
    title="MVC FastAPI App",
    description="FastAPI app with MVC design pattern",
    version="1.0.0",
    lifespan=lifespan  # Attach the lifespan context manager
)

# Add CORS middleware to allow cross-origin requests from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the user authentication routes under the "/auth" path
app.include_router(user_router, prefix="/auth", tags=["Authentication"])

# Include the post management routes under the "/posts" path
app.include_router(post_router, prefix="/posts", tags=["Posts"])
