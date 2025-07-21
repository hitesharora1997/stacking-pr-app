import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer

from app.api.task_router import router as task_router

# Security scheme for API documentation
security = HTTPBearer()

app = FastAPI(
    title="Stacking PR Task API",
    description="A FastAPI application for task management with database integration",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add security middleware (allow testserver for testing)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "testserver",
        "*.herokuapp.com",
        "*.railway.app",
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
    ],  # Add your frontend origins
    allow_credentials=False,  # Set to True if you need credentials
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(task_router, prefix="/api/v1", tags=["tasks"])


@app.get("/", tags=["health"])
def read_root():
    """
    Root endpoint for health checking.

    Returns:
        dict: Health status message
    """
    return {"message": "Hello from FastAPI", "status": "healthy"}


@app.get("/health", tags=["health"])
def health_check():
    """
    Dedicated health check endpoint.

    Returns:
        dict: Application health status
    """
    return {"status": "healthy", "service": "stacking-pr-api", "version": "0.1.0"}


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
