import asyncio
import requests
from agents import Agent, Runner, function_tool

PROFILE_URL = "https://hwm-portfolio-backend-budjdpd9fadsbmf8.malaysiawest-01.azurewebsites.net/profile"

@function_tool
def get_profile() -> str:
    try:
        response = requests.get(PROFILE_URL, timeout=20)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return f'Failed to fetch profile data: {e}'

agent = Agent(
        name = "profile",
        instructions = ("You are serving as a portfolio agent for Hew Wee Ming. You are responsible for answering any queries regarding him from potential recruiters. Be grounded and honest with your responses and avoid overselling him. Use any given tools if necessary to retrieve needed data."),
        tools = [get_profile]
    )

async def main():
    result = await Runner.run(agent, "I am a recruiter from a top AI company based in Singapore, is this candidate suitable for an AI and ML Solution Architect role? Please refer to the job listing here (https://careers.hpe.com/us/en/job/1197428/AI-and-ML-Solution-Architect?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic)")
    print(result.final_output)
    print(f"Answered by: {result.last_agent.name}")

if __name__ == "__main__":
    asyncio.run(main())
