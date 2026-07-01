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
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --shl-primary: #121037;   /* Deep Blue/Purple */
                --shl-accent: #E5005A;    /* SHL Magenta */
                --shl-secondary: #00A3E0; /* SHL Light Blue */
                --text-dark: #2A2A2A;
                --text-light: #FFFFFF;
                --bg-light: #F7F7F7;
            }
            body {
                margin: 0;
                padding: 0;
                font-family: 'Open Sans', sans-serif;
                background-color: var(--bg-light);
                color: var(--text-dark);
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }
            .header {
                width: 100%;
                background-color: var(--text-light);
                padding: 20px 40px;
                box-sizing: border-box;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .logo-container {
                display: flex;
                align-items: center;
                font-family: 'Montserrat', sans-serif;
                font-weight: 800;
                font-size: 32px;
                color: var(--shl-primary);
                letter-spacing: -1px;
                position: relative;
            }
            .logo-arc {
                position: absolute;
                top: -8px;
                left: 10px;
                width: 30px;
                height: 15px;
                border: 4px solid var(--shl-accent);
                border-bottom: none;
                border-radius: 30px 30px 0 0;
            }
            .hero-section {
                background-color: var(--shl-primary);
                color: var(--text-light);
                padding: 80px 40px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            .hero-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(229,0,90,0.2) 0%, rgba(0,163,224,0.2) 100%);
                z-index: 1;
            }
            .hero-content {
                position: relative;
                z-index: 2;
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                font-family: 'Montserrat', sans-serif;
                font-size: 42px;
                font-weight: 800;
                margin-top: 0;
                margin-bottom: 20px;
                line-height: 1.2;
            }
            p {
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .content-wrapper {
                max-width: 1000px;
                width: 100%;
                padding: 60px 40px;
                box-sizing: border-box;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
            }
            .card {
                background: white;
                border-top: 4px solid var(--shl-accent);
                border-radius: 0 0 8px 8px;
                padding: 40px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            .card h2 {
                font-family: 'Montserrat', sans-serif;
                color: var(--shl-primary);
                margin-top: 0;
                font-size: 24px;
            }
            .card p {
                font-size: 15px;
                color: var(--text-dark);
                opacity: 0.8;
            }
            .code-block {
                background-color: #F4F4F4;
                border-left: 4px solid var(--shl-secondary);
                padding: 16px;
                font-family: monospace;
                font-size: 14px;
                color: var(--text-dark);
                margin-bottom: 24px;
                overflow-x: auto;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: var(--shl-accent);
                color: white;
                text-decoration: none;
                padding: 14px 32px;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Montserrat', sans-serif;
                border-radius: 4px;
                transition: background-color 0.3s;
                border: none;
                cursor: pointer;
            }
            .btn:hover {
                background-color: #C0004A;
            }
            .btn-outline {
                background-color: transparent;
                border: 2px solid var(--text-light);
                color: var(--text-light);
            }
            .btn-outline:hover {
                background-color: var(--text-light);
                color: var(--shl-primary);
            }
            .status {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                font-weight: 600;
                color: #2e7d32;
                background: #e8f5e9;
                padding: 8px 16px;
                border-radius: 20px;
                margin-bottom: 20px;
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: #4caf50;
                border-radius: 50%;
            }
            @media (max-width: 768px) {
                .content-wrapper {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo-container">
                <div class="logo-arc"></div>
                SHL
            </div>
            <a href="/docs" class="btn" style="padding: 10px 24px; font-size: 14px;">Developer Portal</a>
        </div>
        
        <div class="hero-section">
            <div class="hero-content">
                <div class="status">
                    <div class="status-dot"></div>
                    Assessment API Online
                </div>
                <h1>Talent Acquisition Intelligence</h1>
                <p>Welcome to the SHL Conversational Agent Backend. Integrate our industry-leading machine learning assessments directly into your hiring workflows.</p>
                <a href="/docs" class="btn btn-outline">Explore API Documentation</a>
            </div>
        </div>
        
        <div class="content-wrapper">
            <div class="card">
                <h2>API Integration</h2>
                <p>
                    Evaluate candidates dynamically through our REST API. Send conversation histories and receive structured competency feedback in real-time.
                </p>
                
                <p style="font-weight: 600; margin-bottom: 8px; margin-top: 24px;">Endpoint Payload Example:</p>
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
            </div>
            
            <div class="card" style="border-top-color: var(--shl-secondary);">
                <h2>Testing & Validation</h2>
                <p>
                    Use the interactive Swagger UI to simulate candidate interactions, review JSON schemas, and test real-time AI responses.
                </p>
                <div style="margin-top: 40px;">
                    <a href="/docs" class="btn">Test Endpoints in /docs</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
