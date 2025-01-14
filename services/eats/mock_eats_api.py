import json
import os
from typing import List
import uuid
from models.order import Order, OrderDetails
from services.eats.eats_api import EatsAPI

class MockEatsAPI(EatsAPI):
    def __init__(self):
        # Load mock data from JSON files
        with open("data/venues.json") as f:
            self.venues = json.load(f)
        with open("data/menus.json") as f:
            self.menus = json.load(f)
        if os.path.exists("tmp/orders.json"):
            with open("tmp/orders.json") as f:
                self.orders = json.load(f)
        else:
            self.orders = {}

    def get_nearby_venues(self, address: str, radius: float) -> List[dict]:
        return self.venues

    def get_menu(self, store_id: str) -> List[dict]:
        return self.menus[store_id]

    def book_order(self, order: Order) -> str:
        order_id = str(uuid.uuid4())
        self.orders[order_id] = {
            "status": "accepted",
            "items": [item.model_dump() for item in order.order_details.items],
            "address": order.order_details.address,
            "total_price": order.order_details.total_price,
            "payment_details": order.payment_details.model_dump(),
        }
        
        with open("tmp/orders.json", "w") as f:
            json.dump(self.orders, f, indent=2)
        
        return order_id

    def check_order(self, order_id: str) -> dict:
        return self.orders.get(order_id, {"status": "not found"})