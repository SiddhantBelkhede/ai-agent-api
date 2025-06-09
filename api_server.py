from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, LLM
from typing import List, Dict, Any, Optional
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint for connectivity testing."""
    return {"status": "ok"}

# In-memory store for conversation history (for demo; use DB for production)
conversation_store: Dict[str, List[Dict[str, Any]]] = {}

class UserData(BaseModel):
    """Model for user financial input data."""
    age: str
    family_members: str
    occupation: str
    total_income: str
    earners: str
    dependents: str
    in_hand_income: str
    investment_percent: str
    investment_methods: str
    dining_out: str
    shopping_freq: str
    recurring_expenses: str
    commute_mode: str
    time_period: str = "monthly"  # default to monthly, can be changed by user
    session_id: Optional[str] = None  # For conversation tracking
    message: Optional[str] = None     # For chat-style input (optional)

@app.post("/generate_plan/")
def generate_plan(user_data: UserData):
    """
    Generate a financial plan based on user data using multiple specialized agents.
    Remembers conversation history using a session_id.
    """
    # Session management
    session_id = user_data.session_id or str(uuid.uuid4())
    if session_id not in conversation_store:
        conversation_store[session_id] = []

    # Store the latest user message (if any)
    if user_data.message:
        conversation_store[session_id].append({"role": "user", "content": user_data.message})
    else:
        # Store the structured user data as a message
        conversation_store[session_id].append({"role": "user", "content": user_data.dict()})

    llm = LLM(model="groq/llama3-70b-8192")

    # Define specialized agents
    expense_analyst = Agent(
        role="Expense Analyst",
        goal="Analyze and categorize all user expenses into Necessities, Luxuries, and Recurring Obligations with realistic Indian values.",
        backstory="A detail-oriented analyst with deep knowledge of Indian household spending patterns.",
        llm=llm,
        verbose=False
    )
    investment_advisor = Agent(
        role="Investment Advisor",
        goal="Recommend optimal investment allocation and methods based on user preferences and Indian market options.",
        backstory="A savvy investment expert who tailors strategies for Indian families.",
        llm=llm,
        verbose=False
    )
    savings_auditor = Agent(
        role="Savings Auditor",
        goal="Audit the user's savings rate, warn if it's below 20%, and suggest actionable ways to improve savings.",
        backstory="A strict but helpful auditor who ensures financial health and future security.",
        llm=llm,
        verbose=False
    )
    lifestyle_adjuster = Agent(
        role="Lifestyle Adjuster",
        goal="Suggest lifestyle adjustments to optimize spending and improve quality of life without sacrificing essentials.",
        backstory="A creative advisor who finds balance between comfort and savings for Indian families.",
        llm=llm,
        verbose=False
    )

    # Task 1: Analyze and categorize expenses
    expense_task = Task(
        description=(
            f"Analyze the following user profile and categorize all monthly expenses into Necessities, Luxuries, and Recurring Obligations. "
            f"Use realistic Indian cost estimates and provide a table with categories, subcategories, and estimated amounts.\n\n"
            f"User Profile:\n"
            f"- Age: {user_data.age}\n"
            f"- Occupation: {user_data.occupation}\n"
            f"- Family Members: {user_data.family_members}\n"
            f"- Earners: {user_data.earners}\n"
            f"- Dependents: {user_data.dependents}\n"
            f"- Monthly In-hand Income: ₹{user_data.in_hand_income}\n"
            f"- Total Family Income: ₹{user_data.total_income}\n"
            f"- Dining Out Frequency: {user_data.dining_out} times/week\n"
            f"- Clothes Shopping Frequency: {user_data.shopping_freq} times/month\n"
            f"- Recurring Expenses: {user_data.recurring_expenses}\n"
            f"- Commute Mode: {user_data.commute_mode}\n"
        ),
        expected_output="A markdown table of categorized expenses with estimated amounts.",
        agent=expense_analyst
    )

    # Task 2: Recommend investment allocation
    investment_task = Task(
        description=(
            f"Based on the user's profile and the expense analysis, recommend how to allocate {user_data.investment_percent}% of income into suitable Indian investment methods: {user_data.investment_methods}. "
            f"Provide a table with method, amount, and rationale."
        ),
        expected_output="A markdown table of investment allocation and rationale.",
        agent=investment_advisor,
        dependencies=[expense_task]
    )

    # Task 3: Audit savings and warn if low
    savings_task = Task(
        description=(
            f"Using the expense and investment breakdown, calculate the user's savings rate. "
            f"If savings are below 20%, warn the user and suggest at least 3 actionable ways to improve savings. "
            f"Summarize savings as a percentage and amount."
        ),
        expected_output="A summary of savings rate, warning if needed, and improvement suggestions.",
        agent=savings_auditor,
        dependencies=[expense_task, investment_task]
    )

    # Task 4: Suggest lifestyle adjustments
    lifestyle_task = Task(
        description=(
            f"Based on the full financial plan, suggest lifestyle adjustments to optimize spending and improve quality of life. "
            f"Be specific and practical for Indian families."
        ),
        expected_output="A bullet list of lifestyle adjustment suggestions.",
        agent=lifestyle_adjuster,
        dependencies=[savings_task]
    )

    # Crew: Run all tasks in order
    crew = Crew(
        agents=[expense_analyst, investment_advisor, savings_auditor, lifestyle_adjuster],
        tasks=[expense_task, investment_task, savings_task, lifestyle_task],
        verbose=False
    )
    try:
        result = crew.kickoff()
        # Store the AI response in the conversation history
        conversation_store[session_id].append({"role": "ai", "content": str(result)})
        return {"success": True, "plan": str(result), "session_id": session_id, "history": conversation_store[session_id]}
    except Exception as e:
        return {"success": False, "error": str(e), "session_id": session_id, "history": conversation_store[session_id]}
