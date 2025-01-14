import pathlib
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings

class AgentEmbeddings:
    def get_embeddings(self) -> Embeddings:
        cache_path = str(pathlib.Path(__file__).parent.parent.parent / "tmp")
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", 
            cache_folder=cache_path
        )