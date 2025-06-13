# Indian Household Financial Planning AI Agent (FastAPI Backend)

A production-ready FastAPI backend for generating structured financial plans for Indian households using multi-agent AI. Designed for easy deployment and integration with Android/mobile apps.

---

## Features
- **Multi-agent AI**: Specialized agents for expense analysis, investment advice, savings audit, and lifestyle adjustment using CrewAI.
- **Session-based conversation**: Maintains conversation history per session using `session_id` (in-memory; can be extended to persistent DB).
- **CORS enabled**: Allows requests from any origin (suitable for Android/mobile integration).
- **Minimal dependencies**: Only essential packages included for security and performance.
- **Secure secrets**: Uses `.env` for API keys and secrets (not tracked by git).
- **Production-ready**: Clean code, ready for deployment and GitHub.

---

## Quick Start

### 1. Clone & Install
```sh
git clone https://github.com/SiddhantBelkhede/ai-agent-api
cd your-repo-name
python -m venv venv
venv\Scripts\activate  # On Windows
# Or: source venv/bin/activate  # On Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Secrets
- Create a `.env` file in the project root with your API keys (see `.gitignore` to ensure it's not tracked).
- Example `.env`:
  ```env
  GROQ_API_KEY=your_groq_api_key
  # Add other secrets as needed
  ```

### 3. Run the API Server
```sh
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### 4. Test the API
- Health check: [https://ai-agent-api-xyyh.onrender.com/health](https://ai-agent-api-xyyh.onrender.com/health)
- Generate plan: POST to [https://ai-agent-api-xyyh.onrender.com/generate_plan/](https://ai-agent-api-xyyh.onrender.com/generate_plan/) with JSON body (see below).

#### Example request (JSON):
```json
{
  "age": "35",
  "familyMembers": "4",
  "gender": "male",
  "occupation": "Engineer",
  "investmentPercentage": 20,
  "investmentOptions": ["SIP", "PPF", "FD"],
  "familyEarners": "2",
  "familyDependents": "2",
  "grossSalary": "120000",
  "expenses": [
    {"name": "Rent", "amount": 25000},
    {"name": "School Fees", "amount": 5000},
    {"name": "Groceries", "amount": 8000}
  ],
  "goals": [
    {"name": "Child's Education", "amount": 1000000, "timeToAchieve": 60},
    {"name": "Car Purchase", "amount": 500000, "timeToAchieve": 24}
  ],
  "session_id": null,
  "message": "I want to save more for my child's education."
}
```
**Response:**
- `success`: true/false
- `plan`: AI-generated financial plan (cleaned for mobile display)
- `session_id`: Use this for follow-up queries
- `history`: Conversation history for the session

---

## API Endpoints

### 1. `/generate_plan/` — Generate Financial Plan
Generate a comprehensive financial plan for an Indian household using multi-agent AI. Maintains session-based conversation history for chat-style interaction.

#### Request (JSON):
```json
{
  "age": "35",
  "familyMembers": "4",
  "gender": "male",
  "occupation": "Engineer",
  "investmentPercentage": 20,
  "investmentOptions": ["SIP", "PPF", "FD"],
  "familyEarners": "2",
  "familyDependents": "2",
  "grossSalary": "120000",
  "expenses": [
    {"name": "Rent", "amount": 25000},
    {"name": "School Fees", "amount": 5000},
    {"name": "Groceries", "amount": 8000}
  ],
  "goals": [
    {"name": "Child's Education", "amount": 1000000, "timeToAchieve": 60},
    {"name": "Car Purchase", "amount": 500000, "timeToAchieve": 24}
  ],
  "session_id": null,
  "message": "I want to save more for my child's education."
}
```
#### Response:
- `success`: true/false
- `plan`: AI-generated financial plan (cleaned for mobile display)
- `session_id`: Use this for follow-up queries
- `history`: Conversation history for the session

---

### 2. `/generate_tip/` — Quick Financial Tip
Get a concise, actionable 1-2 line financial tip for the user based on their profile. No session or chat context required.

#### Request (JSON):
```json
{
  "age": 35,
  "familyMembers": 4,
  "gender": "male",
  "occupation": "salaried",
  "investmentPercentage": 20,
  "investmentOptions": ["PPF", "Mutual Funds"],
  "familyEarners": 1,
  "familyDependents": 2,
  "grossSalary": 1200000,
  "expenses": [
    {"name": "Rent", "amount": 20000},
    {"name": "Groceries", "amount": 8000},
    {"name": "School Fees", "amount": 5000}
  ],
  "goals": [
    {"name": "Child Education", "amount": 1000000, "timeToAchieve": 10},
    {"name": "Retirement", "amount": 5000000, "timeToAchieve": 25}
  ]
}
```
**Response:**
- `success`: true/false
- `tip`: AI-generated 1-2 line financial tip (string only, not an object)

---

## Android/Mobile Integration
- CORS is enabled for all origins (mobile/web friendly).
- Call the API directly from your Android/iOS app using standard HTTP libraries.
- Use the `session_id` from `/generate_plan/` to maintain chat context across requests.
- For quick tips, use `/generate_tip/` with the same user data (excluding `session_id` and `message`).

---

## Deployment

### Free Cloud Options
- [Render](https://render.com/), [Railway](https://railway.app/), [Fly.io](https://fly.io/), [Deta](https://deta.space/), [Vercel](https://vercel.com/) (with serverless support)
- Add your `.env` secrets (e.g., `GROQ_API_KEY`) in the cloud provider's dashboard.
- Use `uvicorn` as the web server.

#### Example: Deploy to Render
1. Push your code to GitHub.
2. Create a new Web Service on Render, connect your repo.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn api_server:app --host 0.0.0.0 --port 10000`
5. Add your `GROQ_API_KEY` in Render's environment settings.

#### Example: Deploy to Railway
1. Push your code to GitHub.
2. Create a new project on Railway, connect your repo.
3. Railway auto-detects FastAPI. Set start command if needed: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
4. Add your `GROQ_API_KEY` in Railway's environment settings.

---

## Security & Best Practices
- **Never commit your `.env` or secrets.**
- For production, use a persistent database for conversation history.
- Review and restrict CORS origins as needed.
- All API keys are loaded from environment variables for security.

---

## Project Structure
```
api_server.py         # Main FastAPI backend
requirements.txt      # Minimal dependencies
tip_agent.py          # Quick tip agent logic
.gitignore            # Excludes .env, __pycache__, etc.
README.md             # This file
.env                  # Your secrets (not tracked by git)
```

---

## Contributing
Pull requests and suggestions are welcome! Please open an issue for major changes.

---

## License
MIT

---

## Author
- SiddhantBelkhede

---

## Credits
- Built with [FastAPI](https://fastapi.tiangolo.com/), [CrewAI](https://github.com/joaomdmoura/crewAI), and [Groq](https://groq.com/).
