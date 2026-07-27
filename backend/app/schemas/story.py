from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class CopilotRequest(BaseModel):
    original_draft: str = Field(..., description="The draft text submitted by the human writer.")
    genre: str = Field("Drama", description="The genre of the story chapter.")
    target_audience: str = Field("Young Adults", description="The target demographic for the story.")
    language: str = Field("english", description="Target language for translation (e.g. tamil, spanish, hindi, english).")
    voice: str = Field("female", description="Voice selection gender: male or female.")
    series_bible: str = Field("", description="Lore, character profiles, or previous chapter summaries for consistency checking.")
    api_key: Optional[str] = Field(None, description="Groq API Key provided by the user.")

class CopilotResponse(BaseModel):
    session_id: str = Field(..., description="Unique run identifier.")
    planner_feedback: str = Field(..., description="Consistency critique and style suggestions.")
    refined_draft: str = Field(..., description="Polished and edited chapter text.")
    localized_draft: str = Field(..., description="Translated story text (if translation occurred).")
    audio_url: Optional[str] = Field(None, description="API URL path to download/stream the generated audio.")
    logs: List[str] = Field(default_factory=list, description="Tracing logs representing nodes visited.")

class RefineRequest(BaseModel):
    draft: str
    series_bible: str = ""
    genre: str = "Drama"
    target_audience: str = "Young Adults"
    api_key: Optional[str] = None


class RefineResponse(BaseModel):
    refined_draft: str
    planner_feedback: str

class TranslateRequest(BaseModel):
    text: str
    target_language: str

class TranslateResponse(BaseModel):
    translated_text: str

class TTSRequest(BaseModel):
    text: str
    language: str = "english"
    voice_gender: str = "female"

class TTSResponse(BaseModel):
    audio_url: str
