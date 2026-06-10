import fitz  # PyMuPDF
import docx
import os
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from utils import FileParsingError, LLMProcessingError

class ProfessionalExperience(BaseModel):
    title: str
    company: str
    duration: str
    bullets: List[str]

class ProjectItem(BaseModel):
    title: str
    technologies: List[str]
    description: str

class EducationItem(BaseModel):
    degree: str
    institution: str
    year: str

class ParsedResumeSchema(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    summary: str = Field(description="Existing professional summary")
    skills: List[str] = Field(description="List of all unique technical and soft skills found")
    experience: List[ProfessionalExperience] = Field(description="List of professional work experiences")
    projects: List[ProjectItem] = Field(description="List of academic or industry projects")
    education: List[EducationItem] = Field(description="List of degrees and educational institutions")
    certifications: List[str] = Field(description="List of certifications acquired")

    model_config = ConfigDict(populate_by_name=True)

def extract_text_from_pdf(file_path: str) -> str:
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise FileParsingError(f"Failed to read PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text])
    except Exception as e:
        raise FileParsingError(f"Failed to read DOCX: {str(e)}")

def parse_resume(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        raw_text = extract_text_from_docx(file_path)
    else:
        raise FileParsingError("Unsupported file format.")
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise LLMProcessingError("Gemini API Key missing in environment context.")

    client = genai.Client(api_key=api_key)
    
    # Retry Mechanism System for 503 errors
    max_retries = 3
    delay = 2
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Extract details from this raw resume text accurately:\n\n{raw_text}",
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert HR Data Extraction Assistant. Extract data exactly as written into the structure provided.",
                    response_mime_type="application/json",
                    response_schema=ParsedResumeSchema,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            # Agar last attempt bhi fail ho jaye toh error throw karein
            if attempt == max_retries - 1:
                raise LLMProcessingError(f"Gemini parsing layer crash after {max_retries} retries: {str(e)}")
            
            # Agar 503 error hai toh ruko aur dobara try karo
            time.sleep(delay)
            delay *= 2  # Exponential backoff (2s -> 4s -> 8s)
