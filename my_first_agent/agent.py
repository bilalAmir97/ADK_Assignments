# Import Modules/components from ADK & GenAI libraries
import asyncio

from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

# Handles rate limiting or temporary service unavailable errors
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)
# Defines root agent/ orchestator agent/ Triage Agent
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="A simple agent that can answer general questions.",
    # system prompt/instructions:
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],  # Tool Calling
)
# Initialize runner to run Triage/Root Agent
runner = InMemoryRunner(agent=root_agent)

# Asynchronous function to handle I/O-bound operations efficiently, like waiting for LLM responses.
async def main():
    # Run the agent with a query and print the detailed debug response.
    response = await runner.run_debug(
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
