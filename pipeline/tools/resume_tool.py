import os
import json # Import the json module
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import your schemas from schemas.py
from pipeline.schemas import  ResumeSchema, ContactInfo

# Import the LLM and structured output functionality
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel as LangchainBaseModel



# --------- Input Schemas for Tools ---------
class DocumentInput(BaseModel):
    """
    Input schema for tools that process a single text documents"""
    text: str = Field(description="The full text extracted from the document (resume ).")


class ResumeExtractorTool(BaseTool):
    """
    A tool to extract structured information from a Resume text.
    """
    name: str = "Resume_Tool"
    description: str = (
        "Use this tool when you need to extract structured information from the text of a Resume."
        "It takes a raw text and returns a JSON object with details like full name, contact info,"
        " education, technical skills, experience, projects, certifications, and summary."
    )

    args_schema: Type[BaseModel] = DocumentInput
    return_direct: bool = True  # The output of this tool is the final answer

    def _run(self, text: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        """
        Identifies the document as a Resume and returns the text for further processing.
        """
        return {"document_type": "resume", "text": text}

    async def _arun(self, text: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        """
        Asynchronously identifies the document as a Resume and returns the text.
        """
        return {"document_type": "resume", "text": text}
