import sys
import os
import json
import pdfplumber
from pipeline.job_parser import JobDescriptionParser
from pipeline.resume_parser import ResumeParser

def read_pdf_text(pdf_path: str) -> str:
    """
    Reads all text from a PDF file using pdfplumber.
    """
    
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    return full_text


def save_to_json(data: dict, filename: str):
    """
    Saves a Python dictionary as a JSON file to the output/ directory.
    """
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"\n JSON saved to: {output_path}")


def main():
    print("Choose option:\n1. Parse Job Description\n2. Parse Resume")
    choice = input("Enter 1 or 2: ")

    pdf_path = input("Enter path to your PDF file (e.g., Dataset/Job_description_DS.pdf): ")

    extracted_text = read_pdf_text(pdf_path)
    print(extracted_text)

    if choice == "1":
        parser = JobDescriptionParser(extracted_text)
        result = parser.parse()
        print("\n Parsed Job Description:\n")
        print(result.model_dump_json(indent=4))
        save_to_json(result.model_dump(), "job_output.json")

    elif choice == "2":
        parser = ResumeParser(extracted_text)
        result = parser.parse()
        print("\n Parsed Resume:\n")
        print(result.model_dump_json(indent=4))
        save_to_json(result.model_dump(), "resume_output.json")

    else:
        print(" Invalid option. Exiting.")


if __name__ == "__main__":
    main()
