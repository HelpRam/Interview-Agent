import pdfplumber
import os
import json # Import json to pretty-print the JSON string
from pipeline.tools.jd_tool import JDExtractorTool
from pipeline.tools.resume_tool import ResumeExtractorTool

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns full text from a PDF file using pdfplumber.
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

if __name__ == "__main__":
    # --- Extract Job Description ---
    jd_file_path = "Dataset/Job_description_DS.pdf"
    print(f"Extracting text from: {jd_file_path}")
    jd_text = extract_text_from_pdf(jd_file_path)

    if jd_text:
        print("\n--- JD Text Extracted ---")
        print(jd_text)

        print("\n--- Running JD Extractor Tool ---")
        jd_tool = JDExtractorTool()
        try:
            extracted_jd_info_json = jd_tool._run(jd_text) # This will now be a JSON string
            print("\n--- Extracted Job Description Information (JSON) ---")
            print(extracted_jd_info_json) 
        except Exception as e:
            print(f"Error running JD Extractor Tool: {e}")
    else:
        print(f"Could not extract text from {jd_file_path}. Skipping JD extraction.")

    print("\n" + "="*50 + "\n") # Separator

    # --- Extract Resume ---
    resume_file_path = "Dataset\\Shashin_Maharjan[AI_CV].pdf" # Make sure you have a resume PDF here
    if not os.path.exists(resume_file_path):
        print(f"Warning: {resume_file_path} not found. Please place a resume PDF in the Dataset folder to test resume extraction.")
    else:
        print(f"Extracting text from: {resume_file_path}")
        resume_text = extract_text_from_pdf(resume_file_path)

        if resume_text:
            print("\n--- Resume Text Extracted ---")
            print(resume_text)

            print("\n--- Running Resume Extractor Tool ---")
            resume_tool = ResumeExtractorTool()
            try:
                extracted_resume_info_json = resume_tool._run(resume_text) # This will now be a JSON string
                print("\n--- Extracted Resume Information (JSON) ---")
                print(extracted_resume_info_json) 
                print(type(extracted_resume_info_json))
            except Exception as e:
                print(f"Error running Resume Extractor Tool: {e}")
        else:
            print(f"Could not extract text from {resume_file_path}. Skipping Resume extraction.")

