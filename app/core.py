# app/core.py

import json
import io
from typing import Dict, Any, List

from app.doc_processor import parse_docx, identify_document_type, add_comments_to_docx
from app.rag_handler import RAGHandler
from config import PROCESS_CHECKLISTS
from app.utils import logger

class CorporateAgent:
    def __init__(self):
        logger.info("Initializing Corporate Agent...")
        self.rag_handler = RAGHandler()
        logger.info("Corporate Agent initialized successfully.")

    def analyze_submission(self, uploaded_files: List) -> Dict[str, Any]:
        """
        Orchestrates the full analysis of a batch of uploaded documents,
        including checklist verification.
        """
        if not uploaded_files:
            return {"error": "No files were uploaded."}

        # --- Step 1: Classify all uploaded documents ---
        classified_docs = []
        for file in uploaded_files:
            text, error = parse_docx(file)
            if error:
                # Skip files that can't be parsed, but log it
                logger.error(f"Skipping unparsable file: {file.name}")
                continue
            doc_type = identify_document_type(text)
            classified_docs.append({"file_name": file.name, "doc_type": doc_type, "text": text, "original_file": file})

        uploaded_doc_types = {doc["doc_type"] for doc in classified_docs}

        # --- Step 2: Determine the legal process and check against the checklist ---
        # (This is a simplified logic; a more advanced version could use an LLM call)
        process_name = "Unknown"
        missing_docs = []
        required_docs = []
        if "Incorporation Application Form" in uploaded_doc_types or "Articles of Association" in uploaded_doc_types:
            process_name = "Company Incorporation"
            required_docs = PROCESS_CHECKLISTS[process_name]
            missing_docs = [doc for doc in required_docs if doc not in uploaded_doc_types]

        # --- Step 3: Create the final consolidated report ---
        submission_report = {
            "process_identified": process_name,
            "documents_uploaded_count": len(classified_docs),
            "required_documents_count": len(required_docs),
            "is_complete": not missing_docs,
            "missing_documents": missing_docs,
            "document_analysis": []
        }

        # --- Step 4: Run individual analysis on each document ---
        for doc in classified_docs:
            logger.info(f"Analyzing individual document: {doc['file_name']}")
            relevant_context = self.rag_handler.retrieve_relevant_docs(doc['text'])
            llm_response_str = self.rag_handler.get_llm_response(doc['text'], relevant_context)

            try:
                analysis_results = json.loads(llm_response_str)
            except json.JSONDecodeError:
                analysis_results = {"error": "Failed to parse analysis from LLM."}

            # Add comments to the docx file if issues are found
            annotated_file_stream = None
            issues = analysis_results.get("issues_found")
            if issues:
                doc['original_file'].seek(0)
                file_stream = io.BytesIO(doc['original_file'].getvalue())
                annotated_file_stream = add_comments_to_docx(file_stream, issues)


            submission_report["document_analysis"].append({
                "file_name": doc['file_name'],
                "document_type": doc['doc_type'],
                "analysis": analysis_results,
                "annotated_file": annotated_file_stream
            })

        return submission_report
