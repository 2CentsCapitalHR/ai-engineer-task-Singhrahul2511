# app/rag_handler.py

import os
import faiss
import json
import re
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from config import (
    CORPUS_DIR, FAISS_INDEX_PATH, EMBEDDING_MODEL,
    LLM_PROVIDER
)
from app.utils import logger

# --- API Key Loading ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ---------------------


class RAGHandler:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.documents = []
        self._load_or_create_vector_store()

    def _load_or_create_vector_store(self):
        """Loads the FAISS index if it exists, otherwise creates it."""
        if os.path.exists(FAISS_INDEX_PATH):
            logger.info("Loading existing FAISS index.")
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            self._process_corpus()
        else:
            logger.info("No FAISS index found. Creating a new one.")
            self._process_corpus()
            self._create_faiss_index()

    def _process_corpus(self):
        """Loads and processes documents from the ADGM corpus directory."""
        loader = DirectoryLoader(
            CORPUS_DIR,
            glob="**/*.docx",
            loader_cls=Docx2txtLoader,
            show_progress=True,
            use_multithreading=True
        )
        docs = loader.load()
        if not docs:
            logger.warning(f"No .docx files found in the corpus directory: {CORPUS_DIR}. The RAG system will have no knowledge base.")
            self.documents = []
            return
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        self.documents = text_splitter.split_documents(docs)
        logger.info(f"Processed {len(self.documents)} document chunks from the corpus.")

    def _create_faiss_index(self):
        """Creates a FAISS index from the processed document chunks."""
        if not self.documents:
            logger.error("Cannot create FAISS index because no documents were loaded from the corpus.")
            return
        logger.info("Creating embeddings for the corpus...")
        embeddings = self.embedding_model.encode([doc.page_content for doc in self.documents])
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        logger.info(f"FAISS index created and saved to {FAISS_INDEX_PATH}")

    def retrieve_relevant_docs(self, query: str, k: int = 5) -> list:
        """Retrieves the top-k relevant document chunks for a given query."""
        if self.index is None or not self.documents:
            logger.error("FAISS index is not initialized or no documents are loaded.")
            return []
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [self.documents[i] for i in indices[0]]

    def get_llm_response(self, user_doc_text: str, relevant_docs: list) -> str:
        """
        Generates a response from the LLM using the user's document and retrieved context.
        """
        if LLM_PROVIDER == "gemini":
            if not GEMINI_API_KEY:
                logger.error("GEMINI_API_KEY not found. Make sure it's set in your .env file.")
                return '{"error": "Server configuration error: Missing Gemini API Key."}'

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                google_api_key=GEMINI_API_KEY,
                timeout=120, # Corrected parameter name from 'request_timeout' to 'timeout'
                model_kwargs={"response_mime_type": "application/json"}
            )

        else:
            raise ValueError("Unsupported LLM provider specified in config.")

        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
        Analyze the **User Submitted Document Text** based on the **ADGM Legal Context**.
        Identify compliance issues, red flags, or missing information.
        Your entire response must be a single, valid JSON object.
        This object must have one key: "issues_found".
        The value of "issues_found" must be a JSON array of objects.
        Each object in the array must contain four string keys: "section", "issue", "severity", and "suggestion".
        Do not include any text, explanations, or markdown formatting before or after the JSON object.

        **ADGM Legal Context:**
        ---
        {context}
        ---

        **User Submitted Document Text:**
        ---
        {user_doc_text}
        ---
        """

        try:
            response = llm.invoke(prompt)
            content = response.content.strip()
            # Use regex to find the JSON object within the string, in case of markdown wrappers
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                clean_json_str = match.group(0)
            else:
                clean_json_str = content

            # This will raise an error if the string is not valid JSON
            json.loads(clean_json_str)
            return clean_json_str
        except json.JSONDecodeError as json_error:
            logger.error(f"LLM response was not valid JSON: {json_error}")
            logger.error(f"Raw LLM response: {response.content}")
            return '{{"issues_found": [{"section": "General", "issue": "The AI model returned a response that was not in the correct format. This may be a temporary issue.", "severity": "Error", "suggestion": "Please try analyzing the document again."}]}}'
        except Exception as e:
            logger.error(f"Error getting response from LLM: {e}", exc_info=True)
            return '{{"error": "An unexpected error occurred while communicating with the AI model."}}'
