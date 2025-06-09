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
- Health check: [http://localhost:8000/health](http://localhost:8000/health)
- Generate plan: POST to `/generate_plan/` with JSON body (see below).

#### Example request (JSON):
```json
{
  "age": "35",
  "family_members": "4",
  "occupation": "Engineer",
  "total_income": "120000",
  "earners": "2",
  "dependents": "2",
  "in_hand_income": "100000",
  "investment_percent": "20",
  "investment_methods": "SIP, PPF, FD",
  "dining_out": "2",
  "shopping_freq": "1",
  "recurring_expenses": "Rent, School Fees",
  "commute_mode": "Car",
  "time_period": "monthly",
  "session_id": null,
  "message": "I want to save more for my child's education."
}
```
**Response:**
- `success`: true/false
- `plan`: AI-generated financial plan
- `session_id`: Use this for follow-up queries
- `history`: Conversation history for the session

---

## Android/Mobile Integration
- CORS is enabled for all origins.
- You can call the API directly from your Android/iOS app using standard HTTP libraries.
- Use the `session_id` to maintain conversation context across requests.

---

## Deployment

### Free Cloud Options
- [Render](https://render.com/), [Railway](https://railway.app/), [Fly.io](https://fly.io/), [Deta](https://deta.space/), [Vercel](https://vercel.com/) (with serverless support)
- Add your `.env` secrets in the cloud provider's dashboard.
- Use `uvicorn` as the web server.

#### Example: Deploy to Render
1. Push your code to GitHub.
2. Create a new Web Service on Render, connect your repo.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn api_server:app --host 0.0.0.0 --port 10000`
5. Add your `GROQ_API_KEY` in Render's environment settings.

---

## Security & Best Practices
- **Never commit your `.env` or secrets.**
- For production, use a persistent database for conversation history.
- Review and restrict CORS origins as needed.

---

## Project Structure
```
api_server.py         # Main FastAPI backend
requirements.txt      # Minimal dependencies
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
