from typing import Dict, List, TypedDict

class CopilotState(TypedDict):
    original_draft: str
    metadata: Dict[str, str]        # Contains 'genre', 'target_audience', 'language', 'voice'
    series_bible: str               # Context on character profiles, world-building, or previous chapters
    planner_feedback: str           # Story planner feedback & consistency checklist
    refined_draft: str              # Polished story draft
    localized_draft: str            # Translated story draft
    audio_path: str                 # Local path to output MP3 narration file
    logs: List[str]                 # Log list showing execution step history
