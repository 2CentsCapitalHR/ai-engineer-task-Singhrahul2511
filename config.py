# config.py

import os

# --- General Configuration ---
PROJECT_NAME = "Corporate Agent"
VERSION = "1.1.0" # Version updated
LOG_LEVEL = "INFO"

# --- Directory Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "adgm_corpus")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")

# --- RAG and LLM Configuration ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_PROVIDER = "gemini"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FAISS_INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "adgm_corpus.faiss")

# --- Document Processing Configuration ---
DOCUMENT_KEYWORDS = {
    "Articles of Association": ["articles of association", "aoa"],
    "Memorandum of Association": ["memorandum of association", "moa"],
    "Board Resolution": ["board resolution", "resolution of the board"],
    "Shareholder Resolution": ["shareholder resolution", "resolution of the shareholders"],
    "Incorporation Application Form": ["incorporation application", "application for incorporation"],
    "UBO Declaration Form": ["ultimate beneficial owner", "ubo declaration"],
    "Register of Members and Directors": ["register of members", "register of directors"],
    "Standard Employment Contract": ["employment contract", "employment agreement"],
    "Change of Registered Address Notice": ["change of registered address", "notice of change of address"],
    "Unknown": []
}

# --- NEW: Legal Process Checklists ---
# This dictionary defines the mandatory documents for key legal processes.
PROCESS_CHECKLISTS = {
    "Company Incorporation": [
        "Articles of Association",
        "Board Resolution",
        "Incorporation Application Form",
        "UBO Declaration Form",
        "Register of Members and Directors"
    ]
    # Add other processes like 'Licensing' or 'Change of Address' here
}
# ------------------------------------

# Ensure required directories exist
for path in [CORPUS_DIR, OUTPUT_DIR, VECTOR_STORE_DIR]:
    os.makedirs(path, exist_ok=True)
