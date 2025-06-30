import re
from typing import List
from .schemas import JobDescription                 # Pydantic model for structured output
from .keywords import (                             # Centralized keyword lists for matching
    CERTIFICATIONS,
    DEGREES,
    SOFT_SKILLS,
    TOOLS_AND_LIBRARIES
)


class JobDescriptionParser:
    """
    A parser class to extract structured information from unstructured job description text.
    """

    def __init__(self, text: str):
        """
        Initialize the parser with raw job description text.
        Text is converted to lowercase for consistent matching.
        """
        self.text = text.lower()

    def parse(self) -> JobDescription:
        """
        Main method that returns a JobDescription Pydantic object,
        filled using multiple helper methods.
        """
        return JobDescription(
            job_title=self.extract_job_title(),
            required_skills=self.extract_required_skills(),
            soft_skills=self.extract_soft_skills(),
            years_of_experience=self.extract_years_of_experience(),
            degree=self.extract_degree(),
            tools_and_platforms=self.extract_tools(),
            certifications=self.extract_certifications()
        )

    def extract_job_title(self) -> str:
        """
        Extracts job title using regex pattern.
        Returns 'Unknown' if not matched.
        """
        match = re.search(r"job title[:\-]?\s*(.*)", self.text)
        return match.group(1).strip() if match else "Unknown"

    def extract_required_skills(self) -> List[str]:
        """
        Extracts technical skills from the job description text.
        Matches keywords from the TOOLS_AND_LIBRARIES list.
        """
        skills = [skill for skill in TOOLS_AND_LIBRARIES if skill in self.text]
        return skills

    def extract_soft_skills(self) -> List[str]:
        """
        Extracts soft skills from the job description text.
        Uses SOFT_SKILLS keyword list for matching.
        """
        return [skill for skill in SOFT_SKILLS if skill in self.text]

    def extract_years_of_experience(self) -> int:
        """
        Uses regex to find patterns like '3+ years of experience'.
        Returns 0 if no match is found.
        """
        match = re.search(r"(\d+)\+?\s+years? of experience", self.text)
        return int(match.group(1)) if match else 0

    def extract_degree(self) -> str:
        """
        Searches for known degree types from DEGREES list.
        Returns the first match or 'Not specified' if none found.
        """
        for degree in DEGREES:
            if degree in self.text:
                return degree.capitalize()
        return "Not specified"

    def extract_tools(self) -> List[str]:
        """
        Identifies tools and platforms mentioned in the text
        using the TOOLS_AND_LIBRARIES list.
        """
        return [tool for tool in TOOLS_AND_LIBRARIES if tool in self.text]

    def extract_certifications(self) -> List[str]:
        """
        Identifies certifications from the CERTIFICATIONS list.
        """
        return [cert for cert in CERTIFICATIONS if cert in self.text]
