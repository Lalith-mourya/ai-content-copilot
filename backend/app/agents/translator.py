from backend.app.agents.state import CopilotState
from backend.app.services.translation import GoogleTranslationService
from backend.app.utils.file_helper import save_story

def translator_node(state: CopilotState) -> dict:
    """
    Translates the refined draft into the specified target language.
    If the target language is English (source language), it is skipped.
    """
    metadata = state.get("metadata", {})
    target_language = metadata.get("language", "english").strip().lower()
    refined_draft = state.get("refined_draft", "")
    
    if not refined_draft.strip() or refined_draft.startswith("Error:"):
        return {
            "localized_draft": refined_draft,
            "logs": state.get("logs", []) + ["TranslatorNode: Skipped translation due to empty or error refined draft."]
        }
        
    if target_language == "english":
        return {
            "localized_draft": refined_draft,
            "logs": state.get("logs", []) + ["TranslatorNode: Skipped translation because target language is English."]
        }
        
    try:
        translator = GoogleTranslationService()
        translated_text = translator.translate(refined_draft, target_lang=target_language, source_lang="english")
        
        # Save locally
        save_story(
            translated_text, 
            filename=f"translated_{target_language}_{metadata.get('genre', 'story').lower().replace(' ', '_')}.md"
        )
    except Exception as e:
        translated_text = f"Failed to translate story to {target_language}: {str(e)}"
        print(f"Error in translator_node: {e}")
        
    logs = state.get("logs", []) + [f"TranslatorNode: Localized chapter translation into {target_language.title()} completed."]
    
    return {
        "localized_draft": translated_text,
        "logs": logs
    }
