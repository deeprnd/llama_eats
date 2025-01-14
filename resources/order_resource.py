import json
import traceback
import uuid
from falcon import Request, Response
import falcon
from services.llm_service import OrderingAgent, Response as AgentResponse, ResponseStatus
from services.eats.eats_api import EatsAPI
from models.order import CCDetails, Order, OrderDetails

class OrderResource:
    def __init__(self, ordering_agent: OrderingAgent, eats_api: EatsAPI):
        self.ordering_agent = ordering_agent
        self.eats_api = eats_api

    def on_post_query(self, req: Request, resp: Response):
        user_ids = req.get_cookie_values("user_id")
        if user_ids:
            user_id = user_ids[0]
        else:
            user_id = str(uuid.uuid4())
        resp.set_cookie("user_id", user_id, max_age=31556952)  # 1 year
        
        input = req.media.get('input')

        if not input:
            resp.status = falcon.HTTP_400
            return

        response = self.ordering_agent.handle_input(user_id, input)
        resp.text = response.model_dump_json()

    def on_post_order(self, req: Request, resp: Response):  
        user_ids = req.get_cookie_values("user_id")
        if user_ids:
            user_id = user_ids[0]
            resp.set_cookie("user_id", user_id, max_age=31556952)  # 1 year
        else:
            resp.status_code = falcon.HTTP_400
            return

        # Get order details from request body
        order_data = req.media
        
        # Validate request payload structure
        if "order" not in order_data or "cc_details" not in order_data:
            resp.status_code = falcon.HTTP_400
            return

        try:
            # Extract payment details from the new payload structure
            cc_data = order_data["cc_details"]
            payment_details = CCDetails.model_validate(cc_data)

            order = order_data["order"]
            order_details = OrderDetails.model_validate(order)         
            order_to_add = Order(id=None,
                            order_details=order_details, 
                            payment_details=payment_details)

            order_id = self.eats_api.book_order(order_to_add)

            success_response = AgentResponse(
                status=ResponseStatus.ORDER_CREATED,
                response=f"Order successfully created with ID: {order_id}",
                order=order_details
            )

            resp.status_code = falcon.HTTP_200
            resp.text = success_response.model_dump_json()
        except KeyError as e:
            resp.status_code = falcon.HTTP_400
        except Exception as e:
            print(e)
            traceback.print_exc()
            resp.status_code = falcon.HTTP_500
