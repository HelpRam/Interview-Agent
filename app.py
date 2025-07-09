import streamlit as st
import json
import pdfplumber
import os
import io

# Assuming these are correctly set up and available in your environment
# Make sure chat_agent.py and pipeline/tools are in your project structure
try:
    from chat_agent import exported_chain as chain, exported_tools as tools
    from pipeline.tools.jd_tool import JDExtractorTool
    from pipeline.tools.resume_tool import ResumeExtractorTool
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.info("Please ensure 'chat_agent.py' and the 'pipeline' directory with 'tools' are correctly placed in your project.")
    st.stop() # Stop the app if essential modules can't be imported

# --------------------- PDF Extraction Utility ---------------------
@st.cache_data
def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text from an uploaded PDF file.
    Uses st.cache_data to cache the result for performance.
    """
    full_text = ""
    try:
        # pdfplumber can open file-like objects directly
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""
    return full_text

# --------------------- Tool and Chain Runners ---------------------
def run_tool_and_chain(tool_class, text, label):
    """
    Runs the specified tool and then the agent chain on the given text.
    Displays results in Streamlit.
    """
    st.subheader(f"Processing {label}")
    tool_output = None
    chain_output = None

    # Find the correct tool instance from the exported_tools list
    tool_instance = next((tool for tool in tools if isinstance(tool, tool_class)), None)

    if not tool_instance:
        st.warning(f"Tool {tool_class.__name__} not found in exported_tools.")
        return tool_output, chain_output

    # Run Manual Tool
    with st.spinner(f"Running {tool_class.__name__} on {label}..."):
        try:
            # The _run method expects a string
            tool_result = tool_instance._run(text)
            tool_output = json.loads(tool_result) # Parse to Python dict
            st.success(f"{tool_class.__name__} completed!")
            st.json(tool_output)

            # Provide download button for tool output
            st.download_button(
                label=f"Download {label} {tool_class.__name__} JSON",
                data=json.dumps(tool_output, indent=2),
                file_name=f"{label.lower().replace(' ', '_')}_{tool_class.__name__.lower().replace('tool', '')}_output.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Error running {tool_class.__name__} on {label}: {e}")

    # Run Agent Chain
    with st.spinner(f"Running Agent Chain on {label}..."):
        try:
            # Ensure chain.invoke is called with correct input format
            chain_result = chain.invoke({
                "input": text,
                "agent_scratchpad": [],
                "chat_history": []
            })
            chain_output = chain_result # Assuming chain_result is already a dict or can be directly displayed
            st.success(f"Agent Chain completed on {label}!")
            st.json(chain_output)

            # Provide download button for chain output
            st.download_button(
                label=f"Download {label} Chain Output JSON",
                data=json.dumps(chain_output, indent=2),
                file_name=f"{label.lower().replace(' ', '_')}_chain_output.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Error running Agent Chain on {label}: {e}")

    return tool_output, chain_output

# --------------------- MAIN STREAMLIT APP ---------------------
def main():
    st.set_page_config(page_title="PDF Extractor & Agent", layout="wide")

    st.title("📄 PDF Extractor & AI Agent for Resumes/JDs")
    st.markdown("""
        Upload your Job Description and Resume PDFs to extract structured information
        and see how the AI agent processes them.
    """)

    # --- File Uploaders ---
    col1, col2 = st.columns(2)

    with col1:
        st.header("Upload Job Description")
        jd_file = st.file_uploader("Upload Job Description PDF", type=["pdf"], key="jd_uploader")
        jd_text = ""
        if jd_file:
            # For pdfplumber, we need a file-like object, not just the UploadedFile object directly
            # We use io.BytesIO to create a byte stream from the uploaded file's content
            jd_bytes = io.BytesIO(jd_file.getvalue())
            jd_text = extract_text_from_pdf(jd_bytes)
            if jd_text:
                st.success("Job Description PDF uploaded and text extracted!")
                with st.expander("View Extracted JD Text"):
                    st.text_area("JD Text", jd_text, height=300)
            else:
                st.warning("Could not extract text from Job Description PDF.")

    with col2:
        st.header("Upload Resume")
        resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="resume_uploader")
        resume_text = ""
        if resume_file:
            resume_bytes = io.BytesIO(resume_file.getvalue())
            resume_text = extract_text_from_pdf(resume_bytes)
            if resume_text:
                st.success("Resume PDF uploaded and text extracted!")
                with st.expander("View Extracted Resume Text"):
                    st.text_area("Resume Text", resume_text, height=300)
            else:
                st.warning("Could not extract text from Resume PDF.")

    st.markdown("---")

    # --- Processing Buttons ---
    st.header("Process Documents")
    process_button = st.button("Run Extraction & Agent")

    if process_button:
        if not jd_file and not resume_file:
            st.warning("Please upload at least one PDF (Job Description or Resume) to process.")
        else:
            st.info("Starting processing...")

            if jd_text:
                st.subheader("--- Job Description Processing Results ---")
                run_tool_and_chain(JDExtractorTool, jd_text, "Job Description")
                st.markdown("---")

            if resume_text:
                st.subheader("--- Resume Processing Results ---")
                run_tool_and_chain(ResumeExtractorTool, resume_text, "Resume")
                st.markdown("---")

            st.success("Processing complete!")

if __name__ == "__main__":
    main()
