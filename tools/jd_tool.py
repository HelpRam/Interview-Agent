import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Optional
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field
from pipeline.job_parser import JobDescriptionParser

class JDInput(BaseModel):
    text: str = Field(..., description="Extracted job description text")

class JobDescriptionParserTool(BaseTool):
    name: str = "JobDescriptionParser"
    description: str = "Parses job description text and extracts job title, skills, experience, and tools."
    args_schema: Optional[ArgsSchema] = JDInput
    return_direct: bool = True

    def run(self, text: str) -> dict:
        parser = JobDescriptionParser(text)
        result = parser.parse()
        return result.dict()

    async def arun(self, text: str) -> dict:
        # Optionally, make this async if JobDescriptionParser supports it
        return self.run(text)

# Example usage
if __name__ == "__main__":
    tool = JobDescriptionParserTool()
    sample_text = "Senior Python Developer with 5 years experience in Django and AWS."
    print(tool.run(sample_text))