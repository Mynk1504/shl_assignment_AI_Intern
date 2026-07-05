# SHL Assessment Conversational Agent

An enterprise-grade, stateless conversational agent API designed to assist users in selecting the most appropriate SHL Individual Test Solutions from the catalog.

## Architecture

This project is built using Domain-Driven Design (DDD) principles for scalability and maintainability:
- **`app/api`**: FastAPI HTTP routes and dependency injection.
- **`app/core`**: Configuration management using `pydantic-settings` and structured logging.
- **`app/models`**: Strict Pydantic schemas validating input/output.
- **`app/services`**: Core business logic, integrating with the Gemini API for LLM responses with `tenacity` exponential backoff.

## Getting Started (Docker)

The easiest way to run the project is via Docker Compose:

1. Clone or copy the project.
2. Create a `.env` file based on the template:
   ```bash
   cp .env.example .env
   ```
3. Add your `GEMINI_API_KEY` to the `.env` file.
4. Run the container:
   ```bash
   docker-compose up --build
   ```
5. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Getting Started (Local Development)

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your environment variables (e.g. `GEMINI_API_KEY`).
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Evaluating Precision & Recall

To verify the agent's performance against expected conversation traces, you can run the evaluation script:
```bash
python scripts/evaluate_metrics.py
```
*(Note: Requires `GEMINI_API_KEY` to be set in your environment variables. Free tier quota limits may apply).*

## Data Management

The agent uses a static, pre-compiled JSON catalog of SHL Individual Test Solutions located at `data/catalog.json`. This ensures fast, reliable, and consistent LLM context injection without the need for runtime web scraping or complex vector databases.
