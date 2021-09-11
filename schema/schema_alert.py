from pydantic import BaseModel


class Alert(BaseModel):
    price: float
