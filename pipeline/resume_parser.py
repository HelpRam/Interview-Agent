import re
from typing import List, Dict
from .schemas import ResumeSchema                      # Pydantic model for resumes
from .keywords import (                                # Keyword lists for matching
    CERTIFICATIONS,
    DEGREES,
    TOOLS_AND_LIBRARIES,
    SOFT_SKILLS
)

class ResumeParser:
    """
    A parser class to extract structured fields from raw resume text.
    """

    def __init__(self, text: str):
        """
        Initializes the ResumeParser with lowercase text for easy matching.
        """
        self.text = text.lower()

    def parse(self) -> ResumeSchema:
        """
        Main method to return a structured ResumeSchema object
        by calling individual extract methods.
        """
        return ResumeSchema(
            full_name=self.extract_full_name(),
            contact_info=self.extract_contact_info(),
            education=self.extract_education(),
            technical_skills=self.extract_technical_skills(),
            experience=self.extract_experience(),
            projects=self.extract_projects(),
            certifications=self.extract_certifications(),
            summary=self.extract_summary()
        )

    def extract_full_name(self) -> str:
        """
        Very basic name extractor: assumes the first non-empty line is the name.
        You can improve this by checking with NER (named entity recognition) later.
        """
        lines = self.text.split('\n')
        for line in lines:
            if line.strip() and len(line.split()) <= 4:  # name likely short
                return line.strip().title()
        return "Unknown"

    def extract_contact_info(self) -> Dict[str, str]:
        """
        Extracts email and phone number from the resume using regex.
        """
        contact = {}

        # Email regex
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", self.text)
        if email_match:
            contact["email"] = email_match.group(0)

        # Phone regex (Nepali and international patterns)
        phone_match = re.search(r"\+?\d[\d\s\-]{7,15}", self.text)
        if phone_match:
            contact["phone"] = phone_match.group(0).strip()

        return contact

    def extract_education(self) -> List[str]:
        """
        Extracts degree-related lines from resume text.
        Matches any line that contains known degree keywords.
        """
        lines = self.text.split('\n')
        education_lines = []

        for line in lines:
            for degree in DEGREES:
                if degree in line:
                    education_lines.append(line.strip())
                    break

        return education_lines

    def extract_technical_skills(self) -> List[str]:
        """
        Returns a list of matched technical tools/libraries from the text.
        """
        return [skill for skill in TOOLS_AND_LIBRARIES if skill in self.text]

    def extract_experience(self) -> List[str]:
        """
        Extracts sentences or lines that mention 'experience'.
        """
        experience_lines = []

        for line in self.text.split('\n'):
            if "experience" in line:
                experience_lines.append(line.strip())

        return experience_lines

    def extract_projects(self) -> List[str]:
        """
        Extracts lines that seem to represent projects.
        Looks for 'project' keyword and collects relevant lines.
        """
        projects = []

        for line in self.text.split('\n'):
            if "project" in line:
                projects.append(line.strip())

        return projects

    def extract_certifications(self) -> List[str]:
        """
        Extracts certifications by checking for keyword matches.
        """
        return [cert for cert in CERTIFICATIONS if cert in self.text]

    def extract_summary(self) -> str:
        """
        Extracts personal summary or objective if present near top.
        Looks for keywords like 'summary', 'objective', etc.
        """
        match = re.search(r"(summary|objective)[:\-]?\s*(.+)", self.text)
        return match.group(2).strip() if match else ""
