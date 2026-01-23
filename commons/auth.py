"""
Authentication Module
=====================
Handles JWT token generation, validation, and user authentication.

You can replace this code with your own authentication implementation.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ============================================================
# CONFIGURATION - Replace with your own secret key in production
# ============================================================
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token security
security = HTTPBearer()


# ============================================================
# PASSWORD UTILITIES
# ============================================================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


# ============================================================
# JWT TOKEN UTILITIES
# ============================================================


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Payload data to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency to get current authenticated user from token

    Usage in routes:
        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"user": user}
    """
    token = credentials.credentials
    payload = decode_token(token)

    # You can add additional user lookup logic here
    # For example, fetch user from database

    return payload


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency to require admin role

    Usage in routes:
        @router.delete("/admin-only")
        async def admin_route(user: dict = Depends(require_admin)):
            return {"admin": user}
    """
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def create_user_token(user_id: str, phone: str, role: str = "customer") -> str:
    """
    Create a token for a pharmacy user

    Args:
        user_id: Unique user identifier
        phone: User's phone number
        role: User role (customer, pharmacist, admin)

    Returns:
        JWT access token
    """
    token_data = {"sub": user_id, "phone": phone, "role": role}
    return create_access_token(token_data)
