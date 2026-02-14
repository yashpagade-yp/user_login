"""
OTP Generator Utility Module

This module provides utility functions for generating OTPs (One-Time Passwords).
"""

import random
from core import logger

logging = logger(__name__)


def generate_otp(length: int = 4) -> str:
    """
    Generate a random numeric OTP of specified length.

    Args:
        length: Length of OTP to generate (default: 4 digits)

    Returns:
        str: A random numeric OTP string

    Example:
        >>> otp = generate_otp(4)
        >>> print(otp)  # e.g., "5832"
    """
    try:
        logging.info(f"Generating {length}-digit OTP")
        # Generate random digits for OTP
        otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
        logging.info("OTP generated successfully")
        return otp
    except Exception as error:
        logging.error(f"Error generating OTP: {str(error)}")
        raise error
