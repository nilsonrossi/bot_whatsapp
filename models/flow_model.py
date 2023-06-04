from datetime import datetime

from pydantic import BaseModel


class FlowModel(BaseModel):
    flow_id: int
    is_new: bool = False
    customer_id: int
    instance_id: str | None = None
    start_date: datetime
    end_date: datetime | None = None
