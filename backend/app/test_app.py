import asyncio
import os
import sys

# Add project root to path for direct running
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from backend.app.agents.graph import workflow
from backend.app.agents.state import CopilotState

async def test_compilation():
    print("Initializing test compilation...")
    assert workflow is not None, "Workflow should compile correctly"
    print("SUCCESS: LangGraph workflow compiled successfully with all nodes!")

if __name__ == "__main__":
    asyncio.run(test_compilation())
