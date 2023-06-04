from pydantic import BaseModel


class CustomerModel(BaseModel):
    customer_id: int
    is_new: bool = False
    profile_name: str
    phone_number: str
    gender_opt: str | None
