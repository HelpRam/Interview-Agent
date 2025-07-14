import json
from chat_agent import chain
import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns all text from the given PDF file.
    """
    full_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""
    return full_text

def run_chain(document_text, label=""):
    print(f"\n--- Running Chain on {label} ---")
    try:
        result = chain.invoke({
            "input": document_text,           # Pass the text!
            "agent_scratchpad": [],
            "chat_history": []
        })
        print(f"\n--- Chain Output on {label} ---")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error running chain on {label}: {e}")

if __name__ == "__main__":
    file_path = input("Provide the path to your document (resume or job description): ").strip()
    if file_path:
        document_text = extract_text_from_pdf(file_path)  # extract actual text
        if document_text:
            run_chain(document_text, label=file_path)     # pass text, 
        else:
            print("No text extracted from the PDF.")
