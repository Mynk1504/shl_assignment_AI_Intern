from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade conversational API for SHL Assessment Selection",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import HTMLResponse

app.include_router(router)
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SHL Assessment AI API</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #20BEFF;
                --text-dark: #202124;
                --text-secondary: #5F6368;
                --bg-light: #F8F9FA;
                --border-color: #DADCE0;
            }
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg-light);
                color: var(--text-dark);
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
            }
            .header {
                width: 100%;
                background-color: white;
                border-bottom: 1px solid var(--border-color);
                padding: 16px 24px;
                box-sizing: border-box;
                display: flex;
                align-items: center;
            }
            .header-title {
                font-size: 18px;
                font-weight: 600;
                color: var(--text-dark);
                margin: 0;
            }
            .content-wrapper {
                max-width: 800px;
                width: 100%;
                padding: 40px 24px;
                box-sizing: border-box;
            }
            .card {
                background: white;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 32px;
                box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
            }
            h1 {
                font-size: 28px;
                font-weight: 700;
                margin-top: 0;
                margin-bottom: 12px;
            }
            p {
                font-size: 15px;
                color: var(--text-secondary);
                line-height: 1.6;
                margin-bottom: 24px;
            }
            .code-block {
                background-color: #F1F3F4;
                border-radius: 4px;
                padding: 16px;
                font-family: monospace;
                font-size: 13px;
                color: var(--text-dark);
                margin-bottom: 24px;
                border: 1px solid var(--border-color);
                overflow-x: auto;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: var(--text-dark);
                color: white;
                text-decoration: none;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 24px;
                transition: background-color 0.2s;
            }
            .btn:hover {
                background-color: #000;
            }
            .status-indicator {
                display: flex;
                align-items: center;
                font-size: 13px;
                color: #137333;
                font-weight: 500;
                margin-bottom: 20px;
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: #1E8E3E;
                border-radius: 50%;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h2 class="header-title">SHL Assessment API</h2>
        </div>
        
        <div class="content-wrapper">
            <div class="card">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    API Service is Running
                </div>
                
                <h1>Conversational Agent Backend</h1>
                <p>
                    This is the backend service for the SHL Assessment conversational agent. 
                    It exposes a machine-to-machine REST API designed to evaluate candidates through structured dialogue.
                </p>
                
                <p style="font-weight: 500; color: var(--text-dark); margin-bottom: 8px;">Quick Start</p>
                <div class="code-block">
POST /chat HTTP/1.1
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I need a test for a Java developer"
    }
  ]
}
                </div>
                
                <p>To interactively test the endpoints, view the schema definitions, and send mock requests, please visit the Swagger documentation.</p>
                
                <a href="/docs" class="btn">Open API Documentation</a>
            </div>
        </div>
    </body>
    </html>
    """
