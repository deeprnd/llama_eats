from typing import Dict, Optional, List

import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from llama_index_client import Document

from models.order import MenuItem
from services.agent.embeddings import AgentEmbeddings

class UserStore:
    def __init__(self, embeddings: AgentEmbeddings):
        self._store: Dict[str, Dict] = {}
        self.user_vector_db: Dict[str, FAISS] = {}
        self.embeddings = embeddings.get_embeddings()
    
    def _ensure_user_exists(self, user_id: str):
        if user_id not in self._store:
            self._store[user_id] = {}
    
    def get_user_vector_db(self, user_id: str) -> FAISS:
        if user_id not in self.user_vector_db:
            index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))
            self.user_vector_db[user_id] = FAISS(
                docstore=InMemoryDocstore(),
                embedding_function=self.embeddings,
                index_to_docstore_id={},
                index=index
            )
        return self.user_vector_db[user_id]
    
    def set_address(self, user_id: str, address: str) -> None:
        self._ensure_user_exists(user_id)
        self._store[user_id]['address'] = address
    
    def set_budget(self, user_id: str, budget: float) -> None:
        self._ensure_user_exists(user_id)
        self._store[user_id]['budget'] = budget
    
    def set_preference(self, user_id: str, preference: str) -> None:
        self._ensure_user_exists(user_id)
        if 'preference' not in self._store[user_id]:
            self._store[user_id]['preference'] = []
        self._store[user_id]['preference'].append(preference)
    
    def set_order(self, user_id: str, order: MenuItem) -> None:
        self._ensure_user_exists(user_id)
        self._store[user_id]['order'] = order
    
    def get_address(self, user_id: str) -> Optional[str]:
        return self._store.get(user_id, {}).get('address')
    
    def get_budget(self, user_id: str) -> Optional[float]:
        return self._store.get(user_id, {}).get('budget')
    
    def get_preferences(self, user_id: str) -> List[str]:
        return self._store.get(user_id, {}).get('preference', [])
    
    def get_order(self, user_id: str) -> Optional[MenuItem]:
        return self._store.get(user_id, {}).get('order')
    
    def has_address(self, user_id: str) -> bool:
        return 'address' in self._store.get(user_id, {})
    
    def has_budget(self, user_id: str) -> bool:
        return 'budget' in self._store.get(user_id, {})
    
    def has_preferences(self, user_id: str) -> bool:
        preferences = self._store.get(user_id, {}).get('preference', [])
        return len(preferences) > 0
    
    def clear_preferences(self, user_id: str) -> None:
        if user_id in self._store and 'preference' in self._store[user_id]:
            self._store[user_id]['preference'] = []
    
    def clear_budget(self, user_id: str) -> None:
        if user_id in self._store and 'budget' in self._store[user_id]:
            del self._store[user_id]['budget']