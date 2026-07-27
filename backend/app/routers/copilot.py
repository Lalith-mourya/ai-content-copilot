import uuid
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from backend.app.schemas.story import (
    CopilotRequest, CopilotResponse,
    RefineRequest, RefineResponse,
    TranslateRequest, TranslateResponse,
    TTSRequest, TTSResponse
)
from backend.app.agents.graph import workflow
from backend.app.agents.state import CopilotState
from backend.app.services.translation import GoogleTranslationService
from backend.app.services.tts import EdgeTTSService
from backend.app.utils.file_helper import get_audio_output_path
from backend.app.agents.planner import planner_node
from backend.app.agents.reviewer import reviewer_node

router = APIRouter(prefix="/api/copilot", tags=["copilot"])

@router.post("/run", response_model=CopilotResponse)
async def run_copilot(payload: CopilotRequest, request: Request):
    """
    Executes the full Copilot Multi-Agent Pipeline.
    1. Plan & check consistency.
    2. Edit & refine draft.
    3. Translate & localize (if needed).
    4. Text-To-Speech audio synthesis.
    """
    session_id = uuid.uuid4().hex[:12]
    
    initial_state = CopilotState(
        original_draft=payload.original_draft,
        metadata={
            "genre": payload.genre,
            "target_audience": payload.target_audience,
            "language": payload.language,
            "voice": payload.voice,
            "api_key": payload.api_key
        },
        series_bible=payload.series_bible,
        planner_feedback="",
        refined_draft="",
        localized_draft="",
        audio_path="",
        logs=[f"System: Workflow initialized for session {session_id}."]
    )
    
    try:
        # Run graph workflow asynchronously
        final_state = await workflow.ainvoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed to complete: {str(e)}")
        
    audio_url = None
    if final_state.get("audio_path"):
        audio_path_obj = Path(final_state["audio_path"])
        filename = audio_path_obj.name
        # Mount location will be /static/audio/{filename}
        audio_url = f"{request.base_url}static/audio/{filename}"
        
    return CopilotResponse(
        session_id=session_id,
        planner_feedback=final_state.get("planner_feedback", ""),
        refined_draft=final_state.get("refined_draft", ""),
        localized_draft=final_state.get("localized_draft", ""),
        audio_url=audio_url,
        logs=final_state.get("logs", [])
    )

@router.post("/refine", response_model=RefineResponse)
async def refine_draft(payload: RefineRequest):
    """
    Executes editorial outline planning and text refinement only.
    """
    temp_state = CopilotState(
        original_draft=payload.draft,
        metadata={
            "genre": payload.genre,
            "target_audience": payload.target_audience,
            "language": "english",
            "voice": "female",
            "api_key": payload.api_key
        },
        series_bible=payload.series_bible,
        planner_feedback="",
        refined_draft="",
        localized_draft="",
        audio_path="",
        logs=[]
    )

    
    try:
        # Invoke nodes sequentially
        planner_res = planner_node(temp_state)
        temp_state.update(planner_res)
        
        reviewer_res = reviewer_node(temp_state)
        temp_state.update(reviewer_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement processing failed: {str(e)}")
        
    return RefineResponse(
        refined_draft=temp_state.get("refined_draft", ""),
        planner_feedback=temp_state.get("planner_feedback", "")
    )

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(payload: TranslateRequest):
    """
    Translates text to a target language.
    """
    try:
        translator = GoogleTranslationService()
        translated = translator.translate(payload.text, target_lang=payload.target_language)
        return TranslateResponse(translated_text=translated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(payload: TTSRequest, request: Request):
    """
    Synthesizes speech audio from input text.
    """
    try:
        output_file = get_audio_output_path()
        tts_service = EdgeTTSService()
        await tts_service.synthesize(
            text=payload.text,
            output_path=output_file,
            voice_gender=payload.voice_gender,
            language=payload.language
        )
        
        filename = Path(output_file).name
        audio_url = f"{request.base_url}static/audio/{filename}"
        return TTSResponse(audio_url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")
