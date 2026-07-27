from backend.app.agents.state import CopilotState
from backend.app.services.tts import EdgeTTSService
from backend.app.utils.file_helper import get_audio_output_path

async def tts_node(state: CopilotState) -> dict:
    """
    Converts localized story chapter text to an audio file (narration).
    Supports asynchronous execution inside LangGraph.
    """
    metadata = state.get("metadata", {})
    language = metadata.get("language", "english").strip().lower()
    voice_gender = metadata.get("voice", "female").strip().lower()
    
    # Narrate localized text if available, fallback to refined text
    text_to_speak = state.get("localized_draft", "").strip()
    if not text_to_speak or text_to_speak.startswith("Error:"):
        text_to_speak = state.get("refined_draft", "").strip()
        
    if not text_to_speak or text_to_speak.startswith("Error:"):
        return {
            "audio_path": "",
            "logs": state.get("logs", []) + ["TTSNode: Skipped narration due to missing or invalid text."]
        }
    
    try:
        # Create output path
        output_file = get_audio_output_path(filename=f"audio_{language}_{voice_gender}.mp3")
        tts_service = EdgeTTSService()
        
        # Await synthesis
        await tts_service.synthesize(
            text=text_to_speak,
            output_path=output_file,
            voice_gender=voice_gender,
            language=language
        )
    except Exception as e:
        output_file = ""
        print(f"Error in tts_node: {e}")
        
    logs = state.get("logs", []) + [f"TTSNode: Narration audiobook generated successfully."]
    
    return {
        "audio_path": output_file,
        "logs": logs
    }
