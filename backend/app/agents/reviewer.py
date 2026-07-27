from backend.app.agents.state import CopilotState
from backend.app.services.llm import get_llm
from backend.app.prompts.reviewer_prompts import REVIEWER_SYSTEM_PROMPT, REVIEWER_USER_TEMPLATE
from backend.app.utils.file_helper import save_story

def reviewer_node(state: CopilotState) -> dict:
    """
    Polishes the draft chapter by integrating the planner's recommendations.
    Ensures grammatical correctness, stylistic refinement, and flow optimization.
    """
    metadata = state.get("metadata", {})
    api_key = metadata.get("api_key")
    llm = get_llm(temperature=0.6, api_key=api_key)  # Balanced temperature for styling and structural editing
    
    genre = metadata.get("genre", "General Drama")

    target_audience = metadata.get("target_audience", "Young Adults")
    
    feedback = state.get("planner_feedback", "")
    original_draft = state.get("original_draft", "")
    
    if not original_draft.strip():
        return {
            "refined_draft": "Error: Original draft is empty.",
            "logs": state.get("logs", []) + ["ReviewerNode: Skip review due to empty original draft."]
        }
        
    user_prompt = REVIEWER_USER_TEMPLATE.format(
        genre=genre,
        target_audience=target_audience,
        feedback=feedback,
        draft=original_draft
    )
    
    messages = [
        {"rolesystem": REVIEWER_SYSTEM_PROMPT},  # Let's fix this dictionary mapping key
        {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    # Filter out any incorrect elements
    messages = [msg for msg in messages if "role" in msg]
    
    try:
        response = llm.invoke(messages)
        refined_text = response.content.strip()
        # Save to local file system
        save_story(refined_text, filename=f"refined_{genre.lower().replace(' ', '_')}.md")
    except Exception as e:
        refined_text = f"Failed to refine draft: {str(e)}"
        print(f"Error in reviewer_node: {e}")
        
    logs = state.get("logs", []) + ["ReviewerNode: Story refinement and line editing completed."]
    
    return {
        "refined_draft": refined_text,
        "logs": logs
    }
