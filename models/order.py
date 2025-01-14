from typing import List, Optional
from pydantic import BaseModel

class CCDetails(BaseModel):
    cc_number: str
    cvv: str
    expiry: str

class MenuItem(BaseModel):
    id: str
    venue_id: str
    title: str
    subtitle: str
    ingredients: List[str]
    price: float
    category: str

class OrderDetails(BaseModel):
    items: List[MenuItem]
    address: str
    total_price: float

class Order(BaseModel):
    id: Optional[str] = None
    order_details: OrderDetails
    payment_details: CCDetails