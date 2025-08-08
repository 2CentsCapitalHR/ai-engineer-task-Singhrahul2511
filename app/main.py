# app/main.py

import sys
import os
import streamlit as st
import json

# --- Path Correction ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------

from app.core import CorporateAgent
from config import OUTPUT_DIR
from app.utils import logger

def main():
    st.set_page_config(
        page_title="Corporate Agent - ADGM Compliance",
        page_icon="🤖",
        layout="wide"
    )

    if 'agent' not in st.session_state:
        with st.spinner("Warming up the AI engine... This may take a moment."):
            st.session_state.agent = CorporateAgent()

    st.sidebar.title("Corporate Agent")
    st.sidebar.info(
        "An AI assistant for ADGM business incorporation and compliance. "
        "Upload all documents for your submission and click 'Analyze'."
    )

    st.title("ADGM Corporate Agent 🤖")
    st.markdown("### Your AI-Powered Legal Compliance Assistant")
    st.markdown("---")

    st.header("1. Upload All Documents for Your Submission")
    uploaded_files = st.file_uploader(
        "Choose your .docx files",
        type=['docx'],
        accept_multiple_files=True
    )

    if st.button("Analyze Submission", disabled=not uploaded_files):
        with st.spinner("Analyzing full submission... This may take a few minutes."):
            try:
                # Call the new submission analysis function
                report = st.session_state.agent.analyze_submission(uploaded_files)

                st.markdown("---")
                st.header("2. Submission Analysis Report")

                # Display the checklist results
                st.subheader("Submission Completeness")
                if report['process_identified'] != "Unknown":
                    st.info(f"**Process Identified:** {report['process_identified']}")
                    if report['is_complete']:
                        st.success("✅ All required documents appear to be present.")
                    else:
                        st.error(f"❌ Missing {len(report['missing_documents'])} required document(s):")
                        for doc in report['missing_documents']:
                            st.markdown(f"- `{doc}`")
                else:
                    st.warning("Could not identify a specific legal process based on the uploaded files.")

                # Display the analysis for each individual document
                st.subheader("Individual Document Review")
                for doc_analysis in report['document_analysis']:
                    with st.expander(f"**File:** `{doc_analysis['file_name']}`", expanded=True):
                        st.success(f"**Identified Document Type:** {doc_analysis['document_type']}")
                        st.json(doc_analysis['analysis'])
                        if doc_analysis.get("annotated_file"):
                            st.download_button(
                                label=f"Download Annotated {doc_analysis['file_name']}",
                                data=doc_analysis["annotated_file"],
                                file_name=f"reviewed_{doc_analysis['file_name']}",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

                # Save the full report
                report_path = os.path.join(OUTPUT_DIR, "submission_report.json")
                # We can't save the file streams in JSON, so we remove them for the report
                for doc in report['document_analysis']:
                    doc.pop('annotated_file', None)
                with open(report_path, 'w') as f:
                    json.dump(report, f, indent=4)
                st.success(f"Full submission report saved to: `{report_path}`")

            except Exception as e:
                logger.error(f"An unexpected error occurred during submission analysis: {e}", exc_info=True)
                st.error("A critical error occurred during the analysis. Please check the logs.")

if __name__ == "__main__":
    main()
