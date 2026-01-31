from fastapi import APIRouter, HTTPException, Depends
from core.apis.schemas.requests.user_request import (
    UserCreateRequest,
    UserLoginRequest,
    UserResetPassword,
    UpdateUserRequest,
    UserForgotPassword,
    VerifyOTPRequest,
    ResetPasswordWithOTPRequest,
)
from core.apis.schemas.responses.user_response import (
    UserCreateResponse,
    PasswordResetResponce,
    UserUpdateResponse,
    UserResponse,
    UserDeleteResponse,
    ForgotPasswordResponse,
)
from core.controllers.user_controller import UserController
from core import logger
from fastapi.security import OAuth2PasswordBearer
from commons.auth import decodeJWT

logging = logger(__name__)

user_router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


@user_router.post("/v1/users", status_code=201, response_model=UserCreateResponse)
async def create_user(request: UserCreateRequest):
    try:
        logging.info("calling /v1/user")
        request = request.model_dump()
        result = await UserController().create_user(request)
        return UserCreateResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in /v1/users endpoint: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post("/v1/user_login", status_code=201, response_model=UserCreateResponse)
async def user_login(login_request: UserLoginRequest):
    try:
        logging.info("calling /v1/user_login")
        login_request = login_request.model_dump()
        result = await UserController().login_user(login_request)
        return UserCreateResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in user_login: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.get("/v1/users/me", response_model=UserResponse)
async def get_user_me(token: str = Depends(oauth2_schema)):
    try:
        logging.info("calling GET /v1/users/me")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        result = await UserController().get_user(user_details.get("id"))
        return UserResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in GET /me: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.patch("/v1/users/me", response_model=UserUpdateResponse)
async def update_user_me(
    request: UpdateUserRequest, token: str = Depends(oauth2_schema)
):
    try:
        logging.info("calling PATCH /v1/users/me")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        result = await UserController().update_user(
            user_details.get("id"), request.model_dump(exclude_none=True)
        )
        return UserUpdateResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in PATCH /me: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.delete("/v1/users/me", response_model=UserDeleteResponse)
async def delete_user_me(token: str = Depends(oauth2_schema)):
    try:
        logging.info("calling DELETE /v1/users/me")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        result = await UserController().delete_user(user_details.get("id"))
        return UserDeleteResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in DELETE /me: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post("/v1/users/reset-password")
async def reset_password(
    request: UserResetPassword,
    token: str = Depends(oauth2_schema),
):
    try:
        logging.info("")

        authenticated_user_details = decodeJWT(token)
        if not authenticated_user_details:
            raise HTTPException(
                status_code=401, detail="Invalid token or token is expired"
            )
        if authenticated_user_details.get("status") != "ACTIVE":
            raise HTTPException(status_code=401, detail="User is not active")
        request = request.model_dump()
        result = await UserController().reset_password(
            request=request, authenticated_user_details=authenticated_user_details
        )
        return PasswordResetResponce(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in reset_password: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


##Forgot Password
@user_router.post(
    "/v1/users/forgot_password", status_code=201, response_model=ForgotPasswordResponse
)
async def forgot_password(forgot_password_request: UserForgotPassword):
    try:
        logging.info("/v1/users/forgot_password")
        forgot_password_request = forgot_password_request.model_dump()
        result = await UserController().forgot_password(forgot_password_request)
        return {**result, "message": "OTP sent successfully"}
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in forgot_password: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post("/v1/users/verify_otp")
async def verify_otp(request: VerifyOTPRequest):
    try:
        logging.info("calling /v1/users/verify_otp")
        request = request.model_dump()
        result = await UserController().verify_otp(request)
        return result
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in verify_otp: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post("/v1/users/reset_password_with_otp")
async def reset_password_with_otp(request: ResetPasswordWithOTPRequest):
    try:
        logging.info("calling /v1/users/reset_password_with_otp")
        request = request.model_dump()
        result = await UserController().reset_password_with_otp(request)
        return result
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in reset_password_with_otp: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
