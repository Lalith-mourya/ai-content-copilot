from langchain_groq import ChatGroq
from backend.app.config import settings

def get_llm(temperature: float = 0.7, api_key: str = None) -> ChatGroq:
    """
    Returns an initialized LangChain ChatGroq model instance.
    Uses user-provided api_key if available, otherwise falls back to environment/configs.
    """
    if not api_key:
        if not settings.GROQ_API_KEY:
            # Fallback to check environment variable directly if setting is empty
            import os
            api_key = os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                raise ValueError("GROQ_API_KEY must be set in the environment or .env file.")
        else:
            api_key = settings.GROQ_API_KEY

    return ChatGroq(
        api_key=api_key,
        model_name=settings.GROQ_MODEL,
        temperature=temperature
    )

