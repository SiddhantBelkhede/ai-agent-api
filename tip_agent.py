from pydantic import BaseModel
from crewai import Agent, LLM, Task
import os

class UserTipData(BaseModel):
    age: str | int
    familyMembers: str | int
    gender: str | int
    occupation: str
    investmentPercentage: float = 0
    investmentOptions: list | dict
    familyEarners: str | int
    familyDependents: str | int
    grossSalary: str | int
    expenses: list[dict]  # Each dict: {"name": str, "amount": float}
    goals: list[dict]     # Each dict: {"name": str, "amount": float, "timeToAchieve": int}

# Initialize LLM with Groq API key from environment
llm = LLM(
    model="groq/llama3-70b-8192",
    api_key=os.environ.get("GROQ_API_KEY")
)

tip_agent = Agent(
    role="Financial Tip Advisor",
    goal="Given the user's financial profile, provide a concise, actionable 1-2 line tip to help them improve their financial health or planning. Be specific and relevant to Indian households.",
    backstory="A friendly financial advisor who gives quick, practical tips for Indian families.",
    llm=llm,
    verbose=False
)

def generate_tip(user_data: UserTipData) -> str:
    prompt = (
        f"User Profile:\n"
        f"- Age: {user_data.age}\n"
        f"- Gender: {user_data.gender}\n"
        f"- Occupation: {user_data.occupation}\n"
        f"- Family Members: {user_data.familyMembers}\n"
        f"- Family Earners: {user_data.familyEarners}\n"
        f"- Family Dependents: {user_data.familyDependents}\n"
        f"- Gross Salary: ₹{user_data.grossSalary}\n"
        f"- Expenses: {user_data.expenses}\n"
        f"- Investment %: {user_data.investmentPercentage}\n"
        f"- Investment Options: {user_data.investmentOptions}\n"
        f"- Goals: {user_data.goals}\n"
        "\nGive a single, actionable tip (1-2 lines) for this user to improve their financial planning."
    )
    # CrewAI expects a string, not a list of Task objects, for single-agent use
    return tip_agent.kickoff(prompt)
