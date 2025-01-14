import logging
import pathlib

from langchain.chains.base import Chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp

from stores.userstore import UserStore

class Chains:
    def __init__(self, user_store: UserStore):
        self.user_store = user_store

    def _get_qa_model(self) -> str:
        base_model_path = pathlib.Path(__file__).parent.parent.parent / "tmp/models--TheBloke--Llama-2-7B-GGUF/snapshots/b4e04e128f421c93a5f1e34ac4d7ca9b0af47b80"
        model_filename = "llama-2-7b.Q6_K.gguf"
        return str(base_model_path / model_filename)
    
    def _get_answer_model(self) -> str:
        base_model_path = pathlib.Path(__file__).parent.parent.parent / "tmp/models--TheBloke--Llama-2-7B-GGUF/snapshots/b4e04e128f421c93a5f1e34ac4d7ca9b0af47b80"
        model_filename = "llama-2-7b.Q8_0.gguf"
        return str(base_model_path / model_filename)
    
    
    def _get_math_model(self) -> str:
        base_model_path = pathlib.Path(__file__).parent.parent.parent / "tmp/models--tensorblock--math_gpt2_sft-GGUF/snapshots/5734d85f95737f5bc347654a26de2822dbc188b5"
        model_filename = "math_gpt2_sft-Q6_K.gguf"
        return str(base_model_path / model_filename)
    
    def create_math_chain(self) -> Chain:
        model_path = self._get_math_model()
        llm = LlamaCpp(model_path=model_path, temperature=0, max_tokens=20, verbose=False, model_kwargs={"loglevel": logging.ERROR})

        prompt_template = """
            Solve the problem of finding the maximum amount from the following input text.
            If the amount is approximate or not clear enough, round up to the next number dividable by 10.
            Reply shortly and to the point, without explaining the reasoning, in 5 words.
            Input Text:
            {input_text}
            Answer:
        """

        prompt = PromptTemplate(
            input_variables=["input_text"],
            template=prompt_template,
        )

        math_chain = prompt | llm
        return math_chain
    
    def create_qa_chain(self, user_id: str) -> Chain:
        model_path = self._get_qa_model()        
        llm = LlamaCpp(model_path=model_path, temperature=0.7, max_tokens=50, verbose=False, model_kwargs={"loglevel": logging.ERROR})

        prompt_template = """
        You are an AI assistant for a food ordering app. Your purpose is to interpret what user wants and user's intent.
        Use the following guide to respond directly to the user without explaining different scenarios. 
        - If the user's input looks like an address (e.g., contains a street number, street name, city, state, and/or zip code), assume they are providing their delivery address.
        - If the user's input mentions food ingredients or cuisine name, assume they are providing information to help select a suitable restaurant and dish.
        - If the user's input mentions a monetary amount or budget (e.g., "50 bucks", "$20", "under 30$"), assume they are providing their budget for the order.
        - If the user's input is not related to ordering food, clarify that your role is to assist with placing food delivery orders.
        - If the user's just provides information, just explain what he's trying to do - don't suggest anything as the next step.
        Use the following pieces of context to determine user's intent:
        {context}
        Reply in less than 50 words to what is the main user's intent based on this user's input:'{question}'
        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        qa_chain = prompt | llm
        return qa_chain
    
    def create_answer_chain(self) -> Chain:
        model_path = self._get_answer_model()        
        llm = LlamaCpp(model_path=model_path, temperature=0.7, max_tokens=100, verbose=False, model_kwargs={"loglevel": logging.ERROR})

        prompt_template = """
        You are an AI assistant for a food ordering app. Your purpose is help user make a purchase.
        Rephrase in words in under 20 words the following response to user in a nicer way and more proffesional way:'{answer}'.
        Repond in words with just with the rephrased single version.
        """
        
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["answer"]
        )

        answer_chain = prompt | llm
        return answer_chain