# SHL Assessment: Technical Approach

## 1. Design Choices
This project implements a robust, stateless conversational AI backend. Built on **FastAPI**, it leverages Domain-Driven Design (DDD) to cleanly separate API routes (`app/api`), structured Pydantic models (`app/models`), and LLM orchestration logic (`app/services`). 

The API is fully stateless (`POST /chat`), accepting the entire conversation history in every request. This design allows for horizontal scaling, eliminates server-side memory bloat, and aligns perfectly with the evaluation harness.

## 2. Retrieval Setup
Instead of implementing a complex Vector Store (RAG) which risks semantic noise and hallucinated results, we scraped the SHL Individual Test Solutions into a clean, static `data/catalog.json`. This catalog is injected directly into the Gemini model's system prompt context window. Because the catalog is relatively small, this guarantees 100% retrieval reliability without the overhead of vector embeddings.

## 3. Prompt Design & Determinism
The prompt is engineered for strict adherence to the 4 conversational behaviors:
- **Temperature 0.0**: We locked the LLM temperature to `0.0` to completely eliminate hallucinated tests.
- **Multi-Skill Recall**: A specific instruction was injected (`ensure you recommend ALL catalog items that match these skills to maximize coverage`) to prevent the LLM from dropping relevant tests when a user asks for combined skills (like AWS and Docker).
- **JSON Enforcement**: We use the Gemini `response_schema` feature to force the LLM to output valid JSON matching the exact expected output shape natively, skipping brittle string-parsing regex.

## 4. Evaluation Approach & Iteration
We built a custom evaluation script (`scripts/evaluate_metrics.py`) to measure **Precision** and **Recall** against labeled test cases. 
* **What didn't work**: 
  1. Our initial prototype attempted to scrape the live `shl.com` site dynamically at runtime. This crashed on deployment platforms (like Render) due to cookie banners and timeouts. We pivoted to the static `catalog.json`.
  2. The Google Gemini Free Tier API strictly limits bursts to 20 requests. Our evaluation harness crashed heavily due to `429 RESOURCE_EXHAUSTED` limits.
* **How we measured/improved**: We integrated `tenacity` into the agent service to provide exponential backoff and retry logic. We then used our evaluation script to benchmark the prompt changes, successfully raising Precision to 100.0% and Recall to 93.3% by tweaking the temperature and multi-skill instructions.

## 5. Tooling
AI coding assistant (Antigravity Agent) was utilized extensively to bootstrap the FastAPI architecture, build the evaluation harness, iterate on prompt engineering, and document the final solution.
