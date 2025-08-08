
Corporate Agent: AI-Powered ADGM Compliance Assistant

## 🚀 Live Demo

**[https://drive.google.com/file/d/1NeSLBgxjiwd4mTgNo3G2GXR5C7yMv1kr/view?usp=sharing]**

Version: 1.1.0
Author: Rahul Singh

Overview
The Corporate Agent is an intelligent legal assistant designed to streamline the business incorporation and compliance process within the Abu Dhabi Global Market (ADGM) jurisdiction. This tool leverages Retrieval-Augmented Generation (RAG) to provide accurate, context-aware analysis of legal documents, ensuring they align with current ADGM laws, regulations, and best practices.

This project was developed as a take-home assignment for the AI Engineer Intern position at 2Cents Capital. It is a production-grade solution that meets all the core requirements outlined in the task sheet.

Demo
A short video demonstrating the application's features and workflow can be found here:

[INSERT YOUR DEMO VIDEO LINK HERE]

Meeting the Requirements
This project was built to precisely match the functional objectives specified in the assignment. Here’s how each requirement is met:

Requirement

How It's Implemented

Accept .docx documents

The Streamlit UI provides a file uploader that accepts multiple .docx files for batch analysis.

Parse and identify document types

The doc_processor.py module parses the text of each document and uses a keyword-based classification system to identify its type (e.g., "Articles of Association").

Check for missing documents

The core.py module identifies the legal process (e.g., "Company Incorporation") and cross-references the uploaded documents against a predefined checklist in config.py. The results are displayed prominently in the UI.

Detect legal red flags

The RAG pipeline in rag_handler.py uses a Gemini LLM to analyze the document's content against a knowledge base of official ADGM documents, identifying inconsistencies, missing clauses, and other red flags.

Insert contextual comments

The doc_processor.py module programmatically inserts styled comments and highlights into a copy of the original .docx file, pinpointing the exact location of each identified issue.

Output a downloadable .docx file

For each analyzed document, the UI provides a download button for the annotated .docx file.

Generate a structured JSON report

The application generates a comprehensive submission_report.json, detailing the checklist results and the full analysis for each document. This file is saved in the output/ directory.

Submission Files
As per the submission checklist, the following example files can be found in the /examples directory of this repository:

Example "Before" Document: An original ADGM template before analysis.

Example "After" Document: The same document after being processed, containing the AI-generated comments.

Example JSON Report: The structured output file corresponding to the analysis.

Screenshot: A screenshot of the application in use.

Project Structure
The project is organized into a modular and scalable architecture for maintainability and future expansion.

corporate-agent/
│
├── 📂 app/                 # Main application source code
│   ├── main.py             # Streamlit UI application
│   └── core.py             # Core business logic and orchestration
│
├── 📂 adgm_corpus/         # Contains the ADGM legal documents for the RAG knowledge base
│
├── 📂 examples/            # Contains example "before" and "after" documents and reports
│
├── 📂 output/              # Default directory for generated reports
│
├── .env                    # Environment variables file (e.g., API keys)
├── config.py               # Centralized configuration for the application
├── requirements.txt        # Python dependencies
└── README.md               # This file



Technologies Used
Backend: Python

Web Framework: Streamlit

LLM Orchestration: LangChain

LLM: Google Gemini 1.5 Flash

Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)

Vector Store: FAISS (Facebook AI Similarity Search)

Document Processing: python-docx

Setup and Installation
1. Prerequisites
Python 3.8+

Git

A Google Gemini API key.

2. Clone the Repository
git clone <your-repository-url>
cd corporate-agent

3. Set Up a Virtual Environment
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Configure Environment Variables
Create a file named .env in the root of the project directory. Add your Google Gemini API key to this file:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

6. Populate the ADGM Corpus
Place all the provided ADGM legal documents (in .docx format) into the adgm_corpus directory. The RAG pipeline will automatically process these files to build its knowledge base on the first run.

How to Run the Application
Start the Streamlit App:
Make sure your virtual environment is activated, then run the following command in the terminal:

streamlit run app/main.py

Using the Application:

Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

Upload a batch of .docx files related to a single legal process.

Click the "Analyze Submission" button.

Review the submission completeness report and the detailed analysis for each document.

Download the annotated .docx files with embedded comments.