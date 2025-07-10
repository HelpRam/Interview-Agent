import os
import json # Import the json module
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun,AsyncCallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema

# Import your schemas from schemas.py
from pipeline.schemas import JobDescription

# Import the LLM and structured output functionality
from langchain_core.pydantic_v1 import BaseModel as LangchainBaseModel



# --------- Input Schemas for Tools ---------
class DocumentInput(BaseModel):
    """
    Input schema for tools that process a single text documents"""
    text: str = Field(description = "The full text extracted from the document ( job description). ")



class JDExtractorTool(BaseTool): 
    """
    A tool to extract structured information from a Job description text.
    """
    name : str = "JD_Tool"
    description : str = (
        "Use this tool when you need to extract structured information from the text of a Job description"
        "It takes a raw text and returns a JSON object with details like Job title, required skills"
        " soft skills, year of experience , degree, tools and platforms, certifications."
    )

    args_schema: Optional[ArgsSchema] = DocumentInput
    return_direct: bool = False  

    def _run(self, text: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:  # Changed return type to str
        """
        Identifies the document as a Job Description and returns the text for further processing.
        """
        result = {"document_type": "job_description", "text": text}
        return json.dumps(result)

    # Asynchronous version of the run method
    async def _arun(self, text: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str: # Changed return type to str
        """
        Asynchronously identifies the document as a Job Description and returns the text.
        """
        result = {"document_type": "job_description", "text": text}
        return json.dumps(result)

