import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

st.title("PDF Comment Extractor (with OCR)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    comments = []

    # Extract annotations first (like before)
    for page_num, page in enumerate(doc, start=1):
        for annot in page.annots() or []:
            comments.append({
                "page": page_num,
                "comment": annot.info.get("content", "")
            })

    # OCR for handwritten / pasted image text
    st.info("Running OCR on each page to detect handwritten/pasted comments...")
    uploaded_file.seek(0)  # reset file pointer
    images = convert_from_bytes(uploaded_file.read())
    for page_num, img in enumerate(images, start=1):
        text = pytesseract.image_to_string(img)
        if text.strip():
            comments.append({
                "page": page_num,
                "comment": text.strip()
            })

    if comments:
        st.success("Comments found in PDF:")
        for c in comments:
            st.write(f"📄 Page {c['page']}: {c['comment']}")
    else:
        st.warning("No comments found in this PDF.")
