# from typing import Optional, Type
# from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
# from langchain_core.tools import BaseTool
# from langchain_core.tools.base import ArgsSchema
# from pydantic import BaseModel, Field
# import pdfplumber

# # --------- Input schemas --------
# from pipeline.schemas import FileInput

# class FileInput(BaseModel):
#     """
#     Input schema for file upload tool.
#     """
#     file_path: str = Field(..., description="The path to the file to be uploaded")

# def extract_text_from_pdf(file_path: str) -> str:
#     """
#     Extracts and returns all text from the given PDF file.
#     """
#     full_text = ""
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             for page in pdf.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     full_text += page_text + "\n"
#     except Exception as e:
#         print(f"Error extracting text from {file_path}: {e}")
#         return ""
#     return full_text

# class ParsingTool(BaseTool):
#     """
#     A tool to handle file uploads and extract text from PDFs.
#     """
#     name: str = "File_Upload_Tool"
#     description: str = "Use this tool to upload a PDF file. It takes a file path and returns the extracted text."
#     args_schema: Optional[ArgsSchema]  = FileInput
#     return_direct: bool = False

#     def _run(self, file_path: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
#         return extract_text_from_pdf(file_path)

#     async def _arun(self, file_path: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
#         # If extract_text_from_pdf is not async, run it in a thread executor
#         from asyncio import to_thread
#         return await to_thread(extract_text_from_pdf, file_path)