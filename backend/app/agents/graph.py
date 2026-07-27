from langgraph.graph import StateGraph, END
from backend.app.agents.state import CopilotState
from backend.app.agents.planner import planner_node
from backend.app.agents.reviewer import reviewer_node
from backend.app.agents.translator import translator_node
from backend.app.agents.tts_agent import tts_node

# Initialize StateGraph with the shared schema
workflow_builder = StateGraph(CopilotState)

# Register agent nodes
workflow_builder.add_node("planner", planner_node)
workflow_builder.add_node("reviewer", reviewer_node)
workflow_builder.add_node("translator", translator_node)
workflow_builder.add_node("tts", tts_node)

# Set up sequential progression flow
workflow_builder.set_entry_point("planner")
workflow_builder.add_edge("planner", "reviewer")
workflow_builder.add_edge("reviewer", "translator")
workflow_builder.add_edge("translator", "tts")
workflow_builder.add_edge("tts", END)

# Compile graph to run as an executable workflow
workflow = workflow_builder.compile()
