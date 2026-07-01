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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-dark: #0f172a;
                --glass-bg: rgba(255, 255, 255, 0.03);
                --glass-border: rgba(255, 255, 255, 0.08);
                --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
            }
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-main);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
                position: relative;
            }
            .blob {
                position: absolute;
                border-radius: 50%;
                filter: blur(80px);
                opacity: 0.4;
                z-index: 0;
                animation: float 10s infinite ease-in-out alternate;
            }
            .blob-1 {
                width: 400px;
                height: 400px;
                background: #3b82f6;
                top: -100px;
                left: -100px;
            }
            .blob-2 {
                width: 500px;
                height: 500px;
                background: #8b5cf6;
                bottom: -150px;
                right: -100px;
                animation-delay: -5s;
            }
            @keyframes float {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(50px, 50px) scale(1.1); }
            }
            .container {
                position: relative;
                z-index: 1;
                background: var(--glass-bg);
                border: 1px solid var(--glass-border);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 24px;
                padding: 3rem;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                opacity: 0;
                transform: translateY(20px);
            }
            @keyframes fadeUp {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            h1 {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -1px;
            }
            p {
                font-size: 1.125rem;
                color: var(--text-muted);
                line-height: 1.6;
                margin-bottom: 2.5rem;
                font-weight: 400;
            }
            .btn {
                display: inline-block;
                background: var(--accent-gradient);
                color: white;
                text-decoration: none;
                padding: 1rem 2.5rem;
                font-size: 1.125rem;
                font-weight: 600;
                border-radius: 9999px;
                transition: all 0.3s ease;
                box-shadow: 0 10px 20px -10px rgba(139, 92, 246, 0.5);
                position: relative;
                overflow: hidden;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 25px -10px rgba(139, 92, 246, 0.7);
            }
            .btn:active {
                transform: translateY(1px);
            }
            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(16, 185, 129, 0.1);
                color: #10b981;
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 0.875rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .pulse {
                width: 8px;
                height: 8px;
                background-color: #10b981;
                border-radius: 50%;
                animation: pulsing 2s infinite;
            }
            @keyframes pulsing {
                0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
                100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="container">
            <div class="status-badge">
                <div class="pulse"></div>
                API System Online
            </div>
            <h1>SHL Assessment AI API</h1>
            <p>Your enterprise-grade conversational agent backend is fully deployed and operational. Experience the power of our structured recommendation engine.</p>
            <a href="/docs" class="btn">Test API in Swagger UI &rarr;</a>
        </div>
    </body>
    </html>
    """
