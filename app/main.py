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
        <title>SHL Assessment API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #FFFFFF;
                color: #2A2A2A;
            }
            .header {
                padding: 20px 40px;
                border-bottom: 1px solid #EAEAEA;
            }
            .logo {
                font-size: 36px;
                font-weight: bold;
                color: #121037; /* SHL Deep Blue */
                position: relative;
                display: inline-block;
                letter-spacing: -1px;
            }
            .logo-arc {
                position: absolute;
                top: -5px;
                left: 5px;
                width: 35px;
                height: 15px;
                border: 5px solid #E5005A; /* SHL Magenta */
                border-bottom: none;
                border-radius: 40px 40px 0 0;
            }
            .container {
                max-width: 800px;
                margin: 60px auto;
                padding: 0 40px;
            }
            h1 {
                color: #121037;
                font-size: 32px;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .btn {
                display: inline-block;
                background-color: #E5005A;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 4px;
            }
            .btn:hover {
                background-color: #C0004A;
            }
            .code {
                background-color: #F7F7F7;
                padding: 15px;
                font-family: monospace;
                border-left: 4px solid #00A3E0; /* SHL Light Blue */
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">
                <div class="logo-arc"></div>
                SHL
            </div>
        </div>
        <div class="container">
            <h1>Assessment API</h1>
            <p>This is the backend service for the SHL conversational agent. It exposes a REST API designed to evaluate candidates through structured dialogue.</p>
            
            <p><strong>Quick Start Example:</strong></p>
            <div class="code">
POST /chat<br>
Content-Type: application/json<br><br>
{<br>
&nbsp;&nbsp;"messages": [<br>
&nbsp;&nbsp;&nbsp;&nbsp;{<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"role": "user",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"content": "I need a test for a Java developer"<br>
&nbsp;&nbsp;&nbsp;&nbsp;}<br>
&nbsp;&nbsp;]<br>
}
            </div>
            
            <p>To interactively test the endpoints, please visit the Developer Documentation page.</p>
            <a href="/docs" class="btn">Go to /docs to test APIs</a>
        </div>
    </body>
    </html>
    """
