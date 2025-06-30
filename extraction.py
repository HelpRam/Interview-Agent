import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns full text from a PDF file using pdfplumber.
    """
    full_text = ""
    
    # Open the PDF
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Append text from each page
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    
    return full_text


extract_text = extract_text_from_pdf("Dataset\Job_description_DS.pdf")
print(extract_text)