from pydantic import BaseModel, Field


class AddressResponse(BaseModel):
    """
    Response schema for user address information.
    """

    street_address: str = Field(
        ..., description="Street address with house/building number"
    )
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State or province")
    postal_code: str = Field(..., description="ZIP or postal code")
    country: str = Field(..., description="Country name")
