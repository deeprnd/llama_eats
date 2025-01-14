import json
import logging
import random
import re
from timeit import default_timer as timer
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel
from transformers.utils import is_torch_mps_available
from langchain.globals import set_verbose
from models.order import MenuItem, OrderDetails
from services.agent.chains import Chains
from services.agent.embeddings import AgentEmbeddings
from services.eats.eats_api import EatsAPI
from sklearn.metrics.pairwise import cosine_similarity
from langchain.docstore.document import Document
from typing import Optional

from enum import Enum

from stores.userstore import UserStore

class IntentEnum(Enum):
    GENERAL_QUESTION = "The user is asking a general question not related to ordering food."
    PROVIDE_ADDRESS = "The user is providing their delivery address or location for their food order."
    PROVIDE_PREFERENCES = "The user is providing their preferred cuisine, type of restaurants or ingredients for their order."
    PROVIDE_BUDGET = "The user is specifying a exact or approximate budget limit or numerical amount they are willing to pay or spend on their food order."

class ResponseStatus(Enum):
    ANSWER = "answer"
    ERROR = "error"
    REQUEST_ADDRESS = "request_address"
    REQUEST_PREFERENCE = "request_preference"
    REQUEST_BUDGET = "request_budget"
    REQUEST_PAYMENT_DETAILS = "request_payment_details"
    ORDER_CREATED = "order_created"

class Response(BaseModel):
    status: ResponseStatus
    response: str
    order: Optional[OrderDetails] = None

class OrderingAgent:
    def __init__(self, eats_api: EatsAPI, chains: Chains, embeddings: AgentEmbeddings, user_store: UserStore):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        set_verbose(False)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if is_torch_mps_available():
            self.logger.debug("MPS is available and being used.")
        else:
            self.logger.warning("MPS is not available or not being used.")
        
        self.eats_api = eats_api
        self.user_store = user_store
        self.chains = chains
        self.embeddings = embeddings.get_embeddings()
        self.enum_embeddings = self.embeddings.embed_documents([e.value for e in IntentEnum])
        self.answer_chain = self.chains.create_answer_chain()

    def _reply(self, answer) -> str:        
        candidate = self.answer_chain.invoke({"answer": answer})
        self.logger.debug(f"\ncandidate answer: {candidate}")
        
        parts = candidate.split('->')
        if len(parts) > 1:
            text_to_search = parts[-1]
        else:
            text_to_search = candidate
            
        pattern = r'(?<!\\)[\'"]((.*?[.!?])+)[\'"]'
        matches = re.findall(pattern, text_to_search)
        valid_matches = [match[0].strip() for match in matches if match[0].strip()]
        if not valid_matches:
            self.logger.warning(f"\ncouldn't rephrase the answer {answer} using candidate answer: {candidate}")
            return answer
        
        return random.choice(valid_matches)
    
    def _parse_budget_amount(self, budget_result: str) -> Optional[float]:
        match = re.search(r'\d+', budget_result)
        if match:
            return int(match.group())
        else:
            return None
        
    def _search_menu_and_order(self, user_id: str) -> Response:
        if not self.user_store.has_address(user_id):
            return Response(status=ResponseStatus.REQUEST_ADDRESS, response=self._reply("Please provide your address."))
        
        if not self.user_store.has_preferences(user_id):
            return Response(status=ResponseStatus.REQUEST_PREFERENCE, response=self._reply("Please provide your food preference."))

        if not self.user_store.has_budget(user_id):
            return Response(status=ResponseStatus.REQUEST_BUDGET, response=self._reply("Please provide your budget."))
        
        user_address = self.user_store.get_address(user_id)
        preferences = self.user_store.get_preferences(user_id)
        budget = self.user_store.get_budget(user_id)

        venues = self.eats_api.get_nearby_venues(
            address=user_address,
            radius=5.0
        )

        # Create a temporary in-memory vector store for menu items
        menu_items = []
        for venue in venues:
            menu = self.eats_api.get_menu(venue["store_id"])
            for item in menu:
                item["venue_id"] = venue["store_id"]
                menu_items.append(Document(page_content=json.dumps(item), metadata=item))

        menu_store = FAISS.from_documents(menu_items, self.embeddings)
        
        combined_preferences = " ".join(preferences)
        self.logger.debug(f"\npreference: {combined_preferences}")
        preference_embedding = self.embeddings.embed_query(combined_preferences)
        docs_and_scores = menu_store.similarity_search_with_score_by_vector(preference_embedding, k=5, filter=lambda metadata: metadata.get('price', float('inf')) <= budget)

        top_item = None
        if docs_and_scores:
            sorted_results = sorted(docs_and_scores, key=lambda x: x[1])
            for doc, score in sorted_results:
                menu_item = MenuItem(**doc.metadata)
                self.logger.debug(f"\nscore: {score} item: {menu_item.title} ingredients: {menu_item.ingredients}")
            
            top_item = MenuItem(**(sorted_results[0][0]).metadata)
        
        if top_item is None:
            self.user_store.clear_preferences(user_id)
            self.user_store.clear_budget(user_id)
            return Response(status=ResponseStatus.ERROR, response=self._reply("Sorry, I couldn't find a dish that matches your preference and budget."))
        
        self.logger.debug(f'selected item: {top_item}')
        order = OrderDetails(items=[top_item], total_price=top_item.price, address=user_address)
        self.user_store.set_order(user_id, order)
        return Response(status=ResponseStatus.REQUEST_PAYMENT_DETAILS, response=self._reply(f"I'll order for you the preferred dish. Please provide payment details - they will sent directly to the payment provider and will not be stored."), order=order)

    def handle_input(self, user_id: str, input_text: str) -> Response:
        self.logger.debug(f'handle_input for {user_id} {input_text}')

        qa_chain = self.chains.create_qa_chain(user_id)

        # Extract user's intent from input
        context = "\n"
        if self.user_store.has_preferences(user_id):
            context += f"User preference is provided.\n"
        else:
            context += f"User hasn't provided yet any food preference, so I don't know what user wants to order.\n"
        
        if self.user_store.has_address(user_id):
            context += f"User address is provided.\n"
        else:
            context += f"User hasn't provided yet any address, so I don't know where to deliver food.\n"
        
        if self.user_store.has_budget(user_id):
            context += f"User budget is provided.\n"
        else:
            context += f"User hasn't provided yet budget, so I don't know the order budget.\n"
            if self.user_store.has_preferences(user_id) and self.user_store.has_address(user_id):
                context += f"Most likely the user's intent will be to provide budget or limit to the order, any number should be considered as order limit.\n"
        
        self.logger.debug(f'context for {user_id} is {context}')
        
        start = timer()
        self.logger.debug(f'intent_chain() invoked')
        intent_description = qa_chain.invoke({
            "question": input_text,
            "context": context
        })
        end = timer()
        self.logger.debug(f'intent_chain() executed in {end - start:.6f} seconds with intent: {intent_description}')

        # Compare intent with enum descriptions using embeddings
        start = timer()
        intent_embeddings = self.embeddings.embed_documents([intent_description])
        similarities = cosine_similarity(intent_embeddings, self.enum_embeddings)
        intent_index = similarities.argmax()
        intent = IntentEnum(list(IntentEnum)[intent_index])
        end = timer()
        self.logger.debug(f'intent_embeddings() executed in {end - start:.6f} seconds with intent: {intent}')

        # Handle different intents
        if intent == IntentEnum.GENERAL_QUESTION:
            general_query_result = qa_chain.invoke({"question": input_text})
            return Response(status=ResponseStatus.ANSWER, response=general_query_result["answer"])

        elif intent == IntentEnum.PROVIDE_BUDGET:
            if not self.user_store.has_budget(user_id):
                budget_input = input_text
                math_chain = self.chains.create_math_chain()
                start = timer()
                budget_result = math_chain.invoke({'input_text': budget_input})
                end = timer()
                self.logger.debug(f'math_chain() executed in {end - start:.6f} seconds with result: {budget_result}')
                budget_amount = self._parse_budget_amount(budget_result)
                if budget_amount is not None:
                    self.user_store.set_budget(user_id, budget_amount)
                    self.logger.debug(f'user {user_id} assigned with budget: {budget_amount}')
                else:
                    return Response(status=ResponseStatus.ERROR, response=self._reply("Sorry, I didn't understand your intent. Could you please rephrase?"))
            return self._search_menu_and_order(user_id)
        
        elif intent == IntentEnum.PROVIDE_ADDRESS:
            if not self.user_store.has_address(user_id):
                self.user_store.set_address(user_id, input_text)
                self.logger.debug(f'user {user_id} assigned with address: {input_text}')        
            return self._search_menu_and_order(user_id)

        elif intent == IntentEnum.PROVIDE_PREFERENCES:
            self.user_store.set_preference(user_id, input_text)
            self.logger.debug(f'user {user_id} assigned with preference: {input_text}')        
            return self._search_menu_and_order(user_id)
        else:
            return Response(status=ResponseStatus.ERROR, response=self._reply("Sorry, I didn't understand your intent. Could you please rephrase?"))