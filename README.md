# SHL Conversational Agent

This is my project for the SHL AI Intern assignment. It's a FastAPI server that helps people find SHL tests by chatting with an agent.

## Setup

1. Install the packages:
```bash
pip install -r requirements.txt
```

2. Set your API key for Gemini:
```bash
# Windows
set GEMINI_API_KEY=your-api-key

# Mac/Linux
export GEMINI_API_KEY=your-api-key
```

3. Start the server:
```bash
uvicorn app:app --port 8000
```

## How it works
- `app.py`: This is the main server. It takes the chat messages and asks Gemini to figure out what the user wants (like their job role and skills). Then it searches the JSON file to find the best tests.
- `scrape_shl.py`: I wrote this to scrape the tests from the SHL website and save them to a JSON file.
- `shl_individual_tests.json`: The data for the tests.
- `test_api.py`: A script to test the chat endpoint.

I used Google's Gemini Flash model because it's fast and can return JSON directly. Instead of using a vector database, I just search the JSON file directly in python to make sure it's fast and doesn't invent fake URLs.
