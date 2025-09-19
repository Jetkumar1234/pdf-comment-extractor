import streamlit as st
import fitz  # PyMuPDF
import easyocr
from pdf2image import convert_from_bytes

st.title("PDF Comment Extractor (with OCR)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # ---- Step 1: Extract digital annotations ----
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    comments = []
    for page_num, page in enumerate(doc, start=1):
        for annot in page.annots() or []:
            comments.append({
                "page": page_num,
                "comment": annot.info.get("content", "")
            })

    # ---- Step 2: OCR for handwritten/pasted comments ----
    st.info("Running OCR on each page... (this may take 10–20 sec on first run)")
    uploaded_file.seek(0)  # reset file pointer for OCR
    images = convert_from_bytes(uploaded_file.read())

    reader = easyocr.Reader(['en'])  # English OCR
    for page_num, img in enumerate(images, start=1):
        text_results = reader.readtext(img)
        text = " ".join([res[1] for res in text_results])
        if text.strip():
            comments.append({"page": page_num, "comment": text.strip()})

    # ---- Step 3: Display results ----
    if comments:
        st.success("✅ Comments found in PDF:")
        for c in comments:
            st.write(f"📄 Page {c['page']}: {c['comment']}")
    else:
        st.warning("⚠️ No comments found in this PDF.")
