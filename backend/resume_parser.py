import pdfplumber
from docx import Document


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_from_docx(file_path)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""


# ------------------ PDF ------------------

def extract_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        print("PDF error:", e)

    return text


# ------------------ DOCX ------------------

def extract_from_docx(file_path):
    text = ""

    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print("DOCX error:", e)

    return text