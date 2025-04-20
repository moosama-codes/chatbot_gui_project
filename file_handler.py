# file_handler.py

def load_file(file_path):
    """
    Loads content from a .txt or .pdf file and returns the text as a string.
    """
    import os
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError("Unsupported file format: Only .txt and .pdf are supported.")


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path):
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
