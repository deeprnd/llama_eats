# test_order_resource.py
import json
import unittest
import uuid
from falcon import testing
from main import create_app
from models.order import OrderDetails
from services.agent.chains import Chains
from services.agent.embeddings import AgentEmbeddings
from services.llm_service import Response, ResponseStatus
from services.eats.mock_eats_api import MockEatsAPI
from stores.userstore import UserStore

class TestOrderResource(unittest.TestCase):
    def setUp(self):
        mock_eats_api = MockEatsAPI()
        embeddings = AgentEmbeddings()
        user_store = UserStore(embeddings)
        chains = Chains(user_store)        
        self.app = create_app(mock_eats_api, chains, embeddings, user_store)
        self.client = testing.TestClient(self.app)

    def _test_order_req(self, user_id, order, cc_details):
        payload = {
            "order": order,
            "cc_details": cc_details
        }

        cookies = {}
        if user_id:
            cookies["user_id"] = str(user_id)

        resp = self.client.simulate_post('/order', cookies=cookies, json=payload)
        self.assertEqual(resp.status_code, 200)
    
    def _test_w_request_for(self, input, next_status, user_id=None, is_order_returned=False):
        payload = {
            "input": input
        }

        cookies = {}
        if user_id:
            cookies["user_id"] = str(user_id)

        resp = self.client.simulate_post('/query', cookies=cookies, json=payload)
        self.assertEqual(resp.status_code, 200)

        response = json.loads(resp.text)
        self.assertIn("status", response)
        self.assertIn("response", response)
        self.assertEqual(response["status"], next_status.value)

        cookies = resp.cookies
        self.assertIn("user_id", cookies)
        cookie_user_id = cookies["user_id"].value
        try:
            user_id_ = uuid.UUID(cookie_user_id)
            if user_id:
                self.assertEqual(user_id, user_id_)

            order = None
            if is_order_returned:
                self.assertIn("order", response)
                response_model = Response(**response)
            
                assert response_model.order is not None, "Order is None in the response"
                assert isinstance(response_model.order, OrderDetails), "Order is not of type OrderDetails"
                order = response_model.order
            
            return user_id_, response["response"], order
        except ValueError:
            self.fail(f"Cookie 'user_id' is not a valid UUID: {cookie_user_id}")
    
    def test_up_to_order_flow1(self):
        user_id, _, _ = self._test_w_request_for("What are some good Italian restaurants nearby?", ResponseStatus.REQUEST_ADDRESS)
        user_id, _, _ = self._test_w_request_for("delivery address is 321 W 54th Street, Apt 2E, New York, NY 10019", ResponseStatus.REQUEST_BUDGET, user_id)
        user_id, _, order = self._test_w_request_for("limit the order under 20$", ResponseStatus.REQUEST_PAYMENT_DETAILS, user_id, True)
        self.assertLessEqual(order.total_price, 20)
        self.assertEqual(len(order.items), 1)

        item = order.items[0]
        self.assertEqual(order.total_price, item.price)
        self.assertEqual(item.category, "italian")

    def test_up_to_order_flow2(self):
        user_id, _, _ = self._test_w_request_for("What are some good Italian restaurants nearby?", ResponseStatus.REQUEST_ADDRESS)
        user_id, _, _ = self._test_w_request_for("something with calamari", ResponseStatus.REQUEST_ADDRESS, user_id)
        user_id, _, _ = self._test_w_request_for("delivery address is 321 W 54th Street, Apt 2E, New York, NY 10019", ResponseStatus.REQUEST_BUDGET, user_id)
        user_id, _, order = self._test_w_request_for("limit the order under 20$", ResponseStatus.REQUEST_PAYMENT_DETAILS, user_id, True)
        self.assertLessEqual(order.total_price, 20)
        self.assertEqual(len(order.items), 1)

        item = order.items[0]
        self.assertEqual(order.total_price, item.price)
        self.assertEqual(item.category, "italian")
        self.assertIn("calamari", item.ingredients)

    def test_order_flow(self):
        user_id, _, _ = self._test_w_request_for("What are some good Italian restaurants nearby?", ResponseStatus.REQUEST_ADDRESS)
        user_id, _, _ = self._test_w_request_for("delivery address is 321 W 54th Street, Apt 2E, New York, NY 10019", ResponseStatus.REQUEST_BUDGET, user_id)
        user_id, _, order = self._test_w_request_for("limit the order under 20$", ResponseStatus.REQUEST_PAYMENT_DETAILS, user_id, True)
        self.assertLessEqual(order.total_price, 20)
        self.assertEqual(len(order.items), 1)

        item = order.items[0]
        self.assertEqual(order.total_price, item.price)
        self.assertEqual(item.category, "italian")

        cc_details = {
            "cc_number": "1231231",
            "cvv": '123',
            "expiry": "12/23"
        }

        self._test_order_req(user_id, order.model_dump(), cc_details)

    def test_order(self):
        user_id = str(uuid.uuid4())
        items = [{
            "id": "8ecd6098-5ef4-4911-8b83-6cad7d1fa731",
            "venue_id": "4a21dd64-2fce-4205-be21-cd9e00159b77",
            "title": "Risotto alla Milanese",
            "subtitle": "Aromatic Roasted Risotto alla Milanese, crafted with a touch of arborio rice, served to perfection.",
            "ingredients": [
                "arborio rice",
                "saffron",
                "onion",
                "white wine",
                "parmesan cheese"
            ],
            "price": 8.22,
            "category": "italian"
            }]
        
        order = {
                "items": items,
                "address": "321 W 54th Street, Apt 2E, New York, NY 10019",
                "total_price": 8.22
            }
        cc_details = {
            "cc_number": "1231231",
            "cvv": '123',
            "expiry": "12/23"
        }

        self._test_order_req(user_id, order, cc_details)