from abc import ABC, abstractmethod
from typing import List
from models.order import Order

class EatsAPI(ABC):
    @abstractmethod
    def get_nearby_venues(self, address: str, radius: float) -> List[dict]:
        pass

    @abstractmethod
    def get_menu(self, store_id: str) -> List[dict]:
        pass

    @abstractmethod
    def book_order(self, order_details: Order) -> str:
        pass

    @abstractmethod
    def check_order(self, order_id: str) -> dict:
        pass