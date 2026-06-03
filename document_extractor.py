
from pypdf import PdfReader
from docx import Document

def load_document(uploaded_file):
    filename=uploaded_file.name.lower()
   

    if filename.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif filename.endswith(".docx"):

        doc = Document(uploaded_file)

        return "\n".join(
            para.text
            for para in doc.paragraphs
        )

    elif filename.endswith(".txt"):

        with open(uploaded_file, "r", encoding="utf-8") as file:
            return file.read()

    else:
        raise ValueError(
            f"Unsupported file format: {filename}. Please upload a PDF, DOCX, or TXT file."
        )
    
