from backend.app.agents.state import CopilotState
from backend.app.services.llm import get_llm
from backend.app.prompts.planner_prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_TEMPLATE

def planner_node(state: CopilotState) -> dict:
    """
    Analyzes the human writer's draft against metadata and the series bible.
    Provides consistency checks, style critique, and improvement outline.
    """
    metadata = state.get("metadata", {})
    api_key = metadata.get("api_key")
    llm = get_llm(temperature=0.3, api_key=api_key)  # Lower temperature for objective editorial checks
    
    genre = metadata.get("genre", "General Drama")

    target_audience = metadata.get("target_audience", "Young Adults")
    series_bible = state.get("series_bible", "No reference bible context provided.")
    original_draft = state.get("original_draft", "")
    
    if not original_draft.strip():
        return {
            "planner_feedback": "Error: Empty draft provided. Unable to perform consistency review.",
            "logs": state.get("logs", []) + ["PlannerNode: Empty draft received."]
        }
        
    user_prompt = PLANNER_USER_TEMPLATE.format(
        genre=genre,
        target_audience=target_audience,
        series_bible=series_bible,
        draft=original_draft
    )
    
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = llm.invoke(messages)
        feedback = response.content
    except Exception as e:
        feedback = f"Failed to generate planner feedback: {str(e)}"
        print(f"Error in planner_node: {e}")
        
    logs = state.get("logs", []) + ["PlannerNode: Consistency check and improvement planning completed."]
    
    return {
        "planner_feedback": feedback,
        "logs": logs
    }
