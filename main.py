import os
import json
import pdfplumber

from chat_agent import exported_chain as chain, exported_tools as tools
from pipeline.tools.jd_tool import JDExtractorTool
from pipeline.tools.resume_tool import ResumeExtractorTool

# --------------------- PDF Extraction Utility ---------------------
def extract_text_from_pdf(file_path: str) -> str:
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

# --------------------- Run Direct Tool (for Debugging) ---------------------
def run_manual_tool(tool_class, text):
    tool = [tool for tool in tools if isinstance(tool, tool_class)][0]
    try:
        result = tool._run(text)
        print(f"\n--- Manual {tool_class.__name__} Output ---")
        print(json.dumps(json.loads(result), indent=2))  # Pretty print
    except Exception as e:
        print(f"Error running {tool_class.__name__}: {e}")

# --------------------- Run Agent Chain ---------------------
def run_chain(text, label=""):
    print(f"\n--- Running Chain on {label} ---")
    try:
        result = chain.invoke({
            "input": text,
            "agent_scratchpad": [],
            "chat_history": []
        })
        print(f"Chain result type: {type(result)}")
        print(f"\n--- Chain Output on {label} ---")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error running chain on {label}: {e}")

# --------------------- MAIN ---------------------
if __name__ == "__main__":
    # --- Resume ---
    resume_path = "Dataset/Ram_Resume_DS.pdf"
    resume_text = extract_text_from_pdf(resume_path)
    if resume_text:
        run_manual_tool(ResumeExtractorTool, resume_text)
        run_chain(resume_text, "Resume")

    # --- Job Description ---
    jd_path = "Dataset/Job_description_DS.pdf"
    jd_text = extract_text_from_pdf(jd_path)
    if jd_text:
        run_manual_tool(JDExtractorTool, jd_text)
        run_chain(jd_text, "Job Description")
