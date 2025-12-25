from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import traceback
from enum import Enum


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorCode(str, Enum):
    # User-related errors
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_INACTIVE = "USER_INACTIVE"
    
    # Authentication errors
    CREDENTIALS_ERROR = "CREDENTIALS_ERROR"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_TOKEN = "INVALID_TOKEN"
    
    # Chapter-related errors
    CHAPTER_NOT_FOUND = "CHAPTER_NOT_FOUND"
    CHAPTER_ALREADY_EXISTS = "CHAPTER_ALREADY_EXISTS"
    
    # Progress-related errors
    PROGRESS_NOT_FOUND = "PROGRESS_NOT_FOUND"
    
    # Simulation-related errors
    SIMULATION_NOT_FOUND = "SIMULATION_NOT_FOUND"
    SIMULATION_CREATION_FAILED = "SIMULATION_CREATION_FAILED"
    
    # Assessment-related errors
    ASSESSMENT_NOT_FOUND = "ASSESSMENT_NOT_FOUND"
    ASSESSMENT_SUBMISSION_ERROR = "ASSESSMENT_SUBMISSION_ERROR"
    
    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: Any, error_code: ErrorCode = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class ErrorHandlingService:
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """Log error with context and traceback"""
        logger.error(f"Error in {context}: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    @staticmethod
    def create_error_response(status_code: int, message: str, error_code: str = None, details: Dict[str, Any] = None):
        """Create a standardized error response"""
        error_response = {
            "error": {
                "message": message,
                "status_code": status_code,
                "error_code": error_code,
                "details": details or {}
            }
        }
        return JSONResponse(status_code=status_code, content=error_response)


# Exception handlers for FastAPI
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.detail}")
    return ErrorHandlingService.create_error_response(
        status_code=exc.status_code,
        message=exc.detail,
        error_code=getattr(exc, 'error_code', None)
    )


async def validation_exception_handler(request, exc):
    logger.error(f"Validation Exception: {exc.errors()}")
    return ErrorHandlingService.create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation error",
        error_code=ErrorCode.VALIDATION_ERROR,
        details={"errors": exc.errors()}
    )


async def general_exception_handler(request, exc):
    logger.error(f"General Exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return ErrorHandlingService.create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal server error",
        error_code=ErrorCode.INTERNAL_ERROR
    )


# Standardized error responses
def raise_user_not_found(username: str):
    raise CustomException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with username '{username}' not found",
        error_code=ErrorCode.USER_NOT_FOUND
    )


def raise_invalid_credentials():
    raise CustomException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        error_code=ErrorCode.CREDENTIALS_ERROR
    )


def raise_token_expired():
    raise CustomException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        error_code=ErrorCode.TOKEN_EXPIRED
    )


def raise_not_implemented(feature: str):
    raise CustomException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Feature '{feature}' is not implemented yet",
        error_code=ErrorCode.NOT_IMPLEMENTED
    )