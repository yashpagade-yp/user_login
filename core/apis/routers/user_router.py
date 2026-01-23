from fastapi import APIRouter, HTTPException
from core.apis.schemas.requests.user_request import UserCreateRequest
from core.apis.schemas.responses.user_response import UserCreateResponse
from core.controllers.user_controller import UserController
from core import logger

logging = logger(__name__)

user_router = APIRouter()


@user_router.post("/v1/users", status_code=201, response_model=UserCreateResponse)
async def create_user(request: UserCreateRequest):
    try:
        logging.info("Calling /v1/users endpoint")
        request = request.model_dump()
        result = await UserController().create_user(request)
        return UserCreateResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in /v1/users endpoint: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
