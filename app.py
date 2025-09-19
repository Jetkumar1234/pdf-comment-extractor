import streamlit as st
import fitz  # PyMuPDF

st.title("PDF Comment Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Open PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    comments = []

    # Loop through pages and extract annotations
    for page_num, page in enumerate(doc, start=1):
        for annot in page.annots() or []:
            comments.append({
                "page": page_num,
                "comment": annot.info.get("content", "")
            })

    if comments:
        st.success("Comments found in PDF:")
        for c in comments:
            st.write(f"📄 Page {c['page']}: {c['comment']}")
    else:
        st.warning("No comments found in this PDF.")
