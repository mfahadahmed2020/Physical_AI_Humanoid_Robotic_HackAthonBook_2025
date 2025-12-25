from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .database import engine
from . import models
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics textbook platform",
    version="1.0.0"
)

# Add various middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, replace with specific hosts
)

# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")

    return response

# Custom middleware for request ID tracking
@app.middleware("http")
async def add_request_id(request, call_next):
    request.state.request_id = str(int(time.time() * 1000000))  # Simple ID based on timestamp
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

@app.get("/")
def read_root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Textbook API"}

# Include routes
from .routes import users, chapters, progress, assessments
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(chapters.router, prefix="/api/v1", tags=["chapters"])
app.include_router(progress.router, prefix="/api/v1", tags=["progress"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}