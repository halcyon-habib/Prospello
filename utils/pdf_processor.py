import fitz  # PyMuPDF
from io import BytesIO

def extract_text_from_pdf(file_object):
    """
    Extracts text from an uploaded PDF file with high accuracy using PyMuPDF.
    """
    try:
        # Read the file bytes from the in-memory uploaded file
        file_bytes = file_object.getvalue()
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text() or ""
            
        pdf_document.close()
        return text
    except Exception as e:
        # Return a more user-friendly error
        return f"Error reading PDF file: {e}. The file might be corrupted or in an unsupported format."

