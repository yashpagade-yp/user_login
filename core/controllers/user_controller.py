from core.cruds.user_crud import UserCRUD
from core.apis.schemas.requests.user_request import UserCreateRequest
from core import logger
from fastapi import HTTPException, status
from commons.auth import encrypt_password, signJWT, verify_password
from core.apis.schemas.requests.user_request import UserLoginRequest
from core.utils.otp_generator import generate_otp
from core.utils.email_service import send_email
from datetime import datetime, timedelta
from core.controllers.order_controller import OrderController

logging = logger(__name__)


class UserController:
    def __init__(self):
        self.UserCRUD = UserCRUD()
        self.OrderController = OrderController()

    async def create_user(self, user_request: dict):
        try:
            logging.info("Executing user_controller.create_user function")
            user = await self.UserCRUD.get_by_email(user_request.get("email", ""))
            if user:
                logging.info("User with this email already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            user_request["hashed_password"] = encrypt_password(
                password=user_request.get("password", "")
            )
            user_request["status"] = "ACTIVE"
            user_request.pop("password", None)
            saved_user = await self.UserCRUD.create(user_request)
            access_token = signJWT(
                id=str(saved_user.id),
                expiry_duration=3600,
                user_status=saved_user.status,
            )
            user_data = saved_user.model_dump()
            user_data["id"] = str(saved_user.id)  # Convert ObjectId to string

            # Fetch orders for the new user (should be empty but good for consistency)
            orders = await self.OrderController.get_user_orders(user_data["id"])

            return {"user": user_data, "access_token": access_token, "orders": orders}
        except Exception as error:
            logging.error(f"Error in user_controller.create_user: {str(error)}")
            raise error

    ##   login user
    async def login_user(self, login_data: dict):
        try:
            logging.info("Executing user_controller.login_user function")
            user = await self.UserCRUD.get_by_email(login_data.get("email", ""))
            if not user:
                logging.info("Login failed: Email not Found")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Email",
                )
                ## verify password
            if not verify_password(
                plain_password=login_data.get("password", ""),
                hashed_password=user.hashed_password,
            ):
                logging.info("Login failed: Incorrect Password")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Password",
                )
            access_token = signJWT(
                id=str(user.id),
                expiry_duration=3600,
                user_status=user.status,
            )
            user_data = user.model_dump()
            user_data["id"] = str(user.id)  # Convert ObjectId to string

            # Fetch orders for the user
            orders = await self.OrderController.get_user_orders(user_data["id"])

            return {"user": user_data, "access_token": access_token, "orders": orders}
        except Exception as error:
            logging.error(f"Error in user_controller.login_user: {str(error)}")
            raise error

    async def get_user(self, user_id: str):
        try:
            logging.info("Executing user_controller.get_user function")
            user = await self.UserCRUD.get_by_id(user_id)
            if not user:
                logging.warning("User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            user_data = user.model_dump()
            user_data["id"] = str(user.id)
            return user_data
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in user_controller.get_user: {str(error)}")
            raise error

    async def update_user(self, user_id: str, update_data: dict):
        try:
            logging.info("Executing user_controller.update_user function")
            updated_user = await self.UserCRUD.update(user_id, update_data)
            if not updated_user:
                logging.warning("User not found or no changes made")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found or no changes made",
                )
            user_data = updated_user.model_dump()
            user_data["id"] = str(updated_user.id)
            return {"user": user_data, "message": "User updated successfully"}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in user_controller.update_user: {str(error)}")
            raise error

    async def delete_user(self, user_id: str):
        try:
            logging.info("Executing user_controller.delete_user function")
            deleted = await self.UserCRUD.delete(user_id)
            if not deleted:
                logging.warning("User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            return {
                "deleted_user_id": user_id,
                "message": "User deleted successfully",
            }
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in user_controller.delete_user: {str(error)}")
            raise error

    ##reset password
    async def reset_password(self, authenticated_user_details: dict, request: dict):
        try:
            logging.info("Executing user_controller.reset_password function")
            user = await self.UserCRUD.get_by_id(
                authenticated_user_details.get("id", "")
            )
            if not user:
                logging.warning("User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            old_password = request.get("old_password", "")
            if not verify_password(old_password, user.hashed_password):
                logging.warning("Invalid old password")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid old password",
                )

            new_password = request.get("new_password", "")
            if len(new_password) < 8:
                logging.warning("New password must be at least 8 characters long")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New password must be at least 8 characters long",
                )

            if old_password == new_password:
                logging.warning("New password must be different from old password")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New password must be different from old password",
                )

            hashed_password = encrypt_password(new_password)

            await self.UserCRUD.update(
                str(user.id), {"hashed_password": hashed_password}
            )
            logging.info("Password reset successfully")
            return {"message": "Password reset successfully"}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in user_controller.reset_password: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    ## FORGOT PASSWORD

    async def forgot_password(self, forgot_password_request: dict):
        try:
            logging.info(
                f"Executing user_controller.forgot_password function for email: {forgot_password_request.get('email')}"
            )
            email = forgot_password_request.get("email", "")
            user = await self.UserCRUD.get_by_email(email)
            if not user:
                logging.warning(f"User not found for email: {email}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            # Generate 4-digit OTP
            otp = generate_otp(4)
            logging.info(f"Generated OTP: {otp} for user: {email}")

            # Set OTP expiry to 5 minutes from now
            otp_expiry = datetime.utcnow() + timedelta(minutes=5)

            # Store OTP in database
            logging.info("Storing OTP in database...")
            await self.UserCRUD.update_otp(email, otp, otp_expiry)
            logging.info("OTP stored in database successfully")

            # Send OTP via email
            logging.info("Preparing to send email...")
            subject = "Password Reset OTP"
            from core.utils.email_templates import get_otp_email_template

            # Get user's name for personalization
            user_name = f"{user.first_name} {user.last_name}"
            html_content = get_otp_email_template(otp, user_name)

            text = f"Your OTP for password reset is: {otp}. This OTP is valid for 5 minutes."
            logging.info(f"Calling send_email for {email}")
            await send_email(subject, email, text, html_content)
            logging.info(f"OTP sent successfully to email: {email}")

            return {"email": email}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(
                f"Error in user_controller.forgot_password: {str(error)}", exc_info=True
            )
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(error)}"
            )

    async def verify_otp(self, verify_request: dict):
        try:
            logging.info(
                f"Executing verify_otp for email: {verify_request.get('email')}"
            )
            email = verify_request.get("email")
            otp = verify_request.get("otp")

            user = await self.UserCRUD.get_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if not user.otp or user.otp != otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")

            if user.otp_expiry < datetime.utcnow():
                raise HTTPException(status_code=400, detail="OTP has expired")

            return {"message": "OTP verified successfully"}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in verify_otp: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def reset_password_with_otp(self, reset_request: dict):
        try:
            logging.info(
                f"Executing reset_password_with_otp for email: {reset_request.get('email')}"
            )
            email = reset_request.get("email")
            otp = reset_request.get("otp")
            new_password = reset_request.get("new_password")

            user = await self.UserCRUD.get_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if not user.otp or user.otp != otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")

            if user.otp_expiry < datetime.utcnow():
                raise HTTPException(status_code=400, detail="OTP has expired")

            # Update password and clear OTP
            hashed_password = encrypt_password(new_password)
            update_data = {
                "hashed_password": hashed_password,
                "otp": None,
                "otp_expiry": None,
            }

            await self.UserCRUD.update_otp(email, None, None)  # Clear OTP
            await self.UserCRUD.update(
                str(user.id), {"hashed_password": hashed_password}
            )

            return {"message": "Password reset successful"}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in reset_password_with_otp: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")
