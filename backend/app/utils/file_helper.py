import os
import uuid
from pathlib import Path
from backend.app.config import settings

def save_story(content: str, filename: str = None) -> str:
    """
    Saves story content to the outputs/stories directory.
    Returns the absolute string path to the saved file.
    """
    if not filename:
        filename = f"story_{uuid.uuid4().hex[:8]}.md"
    if not filename.endswith((".md", ".txt")):
        filename += ".md"
        
    file_path = settings.OUTPUT_DIR / "stories" / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)

def get_audio_output_path(filename: str = None) -> str:
    """
    Generates a writeable filepath for audio outputs.
    """
    if not filename:
        filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
    if not filename.endswith((".mp3", ".wav")):
        filename += ".mp3"
        
    file_path = settings.OUTPUT_DIR / "audio" / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return str(file_path)
