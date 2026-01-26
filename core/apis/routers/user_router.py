from fastapi import APIRouter, HTTPException
from core.apis.schemas.requests.user_request import UserCreateRequest
from core.apis.schemas.responses.user_response import UserCreateResponse
from core.controllers.user_controller import UserController
from core import logger

logging = logger(__name__)

# Correctly using APIRouter
user_router = APIRouter()


@user_router.post("/v1/users", status_code=201, response_model=UserCreateResponse)
async def create_user(request: UserCreateRequest):
    try:
        logging.info("Calling /v1/users endpoint")
        user_data = request.model_dump()
        result = await UserController().create_user(user_data)
        return UserCreateResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in User_create: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post("/v1/login")
async def login_user(signin: UserLoginRequest):
    try:
        logging.info("Calling /v1/login endpoint")
        login_data = signin.model_dump()
        result = await UserController().login_user(login_data)
        return UserLoginResponce(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error on User Create: {str(e)}")
        raise HTTPException(sataus_code=500, detail="Internal Server Error")
