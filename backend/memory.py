import os
from langchain_community.vectorstores import FAISS
# CHANGE: Use local HuggingFace embeddings instead of Google API
from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.docstore.document import Document

class ClaireMemory:
    def __init__(self):
        # Initialize FREE local embeddings (runs on your laptop)
        # "all-MiniLM-L6-v2" is fast and lightweight
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None

    def add_memory(self, text: str):
        """Adds a user interaction to long-term memory."""
        doc = Document(page_content=text)
        if self.vector_db is None:
            self.vector_db = FAISS.from_documents([doc], self.embeddings)
        else:
            self.vector_db.add_documents([doc])

    def retrieve_context(self, query: str, k=2):
        """Finds relevant past conversations."""
        if self.vector_db is None:
            return ""
        # Search the vector DB
        docs = self.vector_db.similarity_search(query, k=k)
        return "\n".join([d.page_content for d in docs])