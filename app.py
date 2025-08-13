import streamlit as st
import os
from langgraph_workflow import build_graph
from utils import extract_pdf_text, export_slides
import tempfile

st.set_page_config(page_title="PDF to Slide Generator", layout="centered")

st.title("📄→📊 PDF to Slide Generator (LangGraph + Gemini)")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    st.success("✅ PDF Uploaded!")
    document_text = extract_pdf_text(temp_pdf_path)
    st.text_area("📜 Extracted Text", document_text[:1000], height=200)

    if st.button("🚀 Generate Slides"):
        with st.spinner("Processing with Gemini..."):
            graph = build_graph()
            input_state = {"text": document_text, "sections": [], "slides": []}
            output = graph.invoke(input_state)
            pptx_path = export_slides(output["slides"])
            st.success("✅ Slides generated!")

            with open(pptx_path, "rb") as f:
                st.download_button("📥 Download PPTX", f, file_name="generated_slides.pptx")
