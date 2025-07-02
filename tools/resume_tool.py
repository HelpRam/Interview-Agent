
from typing import Optional
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field
from pipeline.resume_parser import ResumeParser

class ResumeInput(BaseModel):
    text: str = Field(..., description="Extracted resume text")

class ResumeParserTool(BaseTool):
    name: str = "ResumeParser"
    description: str = "Parses resume text and extracts fields like name, contact, education, and skills."
    args_schema: Optional[ArgsSchema] = ResumeInput
    return_direct: bool = True

    def _run(self, text: str, run_manager=None) -> dict:
        parser = ResumeParser(text)
        result = parser.parse()
        return result.dict()

    async def _arun(self, text: str, run_manager=None) -> dict:
        return self._run(text)
