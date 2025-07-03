import os
import json # Import the json module
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import your schemas from schemas.py
from pipeline.schemas import JobDescription

# Import the LLM and structured output functionality
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel as LangchainBaseModel


# --- Tool Setup ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

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

    args_schema: Type[BaseModel] = DocumentInput
    return_direct: bool = True  # The output of this tool is the final answer

    def _run(self, text:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str: # Changed return type to str
        """ Use the tool."""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert at extracting information from documents."
                    "Analyze the following Job description text and extract the key details"
                    "into the provided JSON schema. Pay close attention to required skills,"
                    "soft skills, year of experience , degree, tools and platforms, certifications."

                ),
                (
                    "user", "{jd_text}"
                )
            ]
        )

        # chain the prompt with the LLM ad the structured output schema
        extractor_chain = prompt | llm.with_structured_output(JobDescription)

        # Invoke the chain with the input text
        result = extractor_chain.invoke({"jd_text": text})

        return json.dumps(result.dict(), indent=4) # Convert dict to JSON string with indentation

    # Asynchronous version of the run method
    async def _arun(self, text: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str: # Changed return type to str
        """ Use the tool asynchronously."""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert at extracting information from documents."
                    "Analyze the following Job description textand extract the key details "
                    " into the provided JSON schema."

                ),
                (
                    "user", "{jd_text}"
                )
            ]

        )
        extractor_chain = prompt | llm.with_structured_output(JobDescription)
        result = await extractor_chain.ainvoke({"jd_text": text})

        return json.dumps(result.dict(), indent=4) # Convert dict to JSON string with indentation
