import os
import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional

try:
    import google.generativeai as genai
    HAS_LLM = True
except ImportError:
    HAS_LLM = False

app = FastAPI()

# load catalog
try:
    with open("shl_individual_tests.json", "r", encoding="utf-8") as f:
        CATALOG = json.load(f)
except Exception as e:
    print("error loading catalog:", e)
    CATALOG = []

# schemas
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class Assessment(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Assessment] = []
    end_of_conversation: bool

# extracted info from llm
class ExtractedContext(BaseModel):
    intent: str
    role: Optional[str] = None
    seniority: Optional[str] = None
    skills: List[str] = []
    test_preferences: List[str] = []
    comparison_tests: List[str] = []

def is_out_of_scope(messages):
    last_msg = messages[-1].content.lower()
    bad_words = ['salary', 'legal', 'lawsuit', 'pay', 'ignore previous', 'prompt injection']
    for word in bad_words:
        if word in last_msg:
            return True
    return False

def retrieve_assessments(context: ExtractedContext):
    scored = []
    role = (context.role or "").lower()
    seniority = (context.seniority or "").lower()
    skills = [s.lower() for s in context.skills]
    prefs = [p.lower() for p in context.test_preferences]

    for test in CATALOG:
        score = 0
        desc = test.get("description", "").lower()
        test_skills = " ".join(test.get("skills", [])).lower()
        test_levels = " ".join(test.get("job_levels", [])).lower()
        test_type = test.get("test_type", "").lower()
        
        text_to_search = desc + " " + test_skills
        
        if seniority and seniority in test_levels:
            score += 3
            
        for skill in skills:
            if skill in text_to_search:
                score += 2
                
        if role and role in text_to_search:
            score += 1
            
        if prefs:
            if "personality" in prefs and "p" in test_type:
                score += 2
            elif "cognitive" in prefs and "a" in test_type:
                score += 2
            elif "technical" in prefs and "k" in test_type:
                score += 2
            
        if score > 0:
            scored.append((score, test))
            
    # sort by highest score first
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # get top 10
    top_tests = []
    for s, t in scored[:10]:
        top_tests.append(t)
    return top_tests

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # check if they are asking something out of scope
    if is_out_of_scope(request.messages):
        return ChatResponse(
            reply="I am an SHL assessment recommender. I cannot help with salary or legal questions.",
            recommendations=[],
            end_of_conversation=False
        )
        
    # turn history into a string
    history_str = ""
    for m in request.messages:
        history_str += f"{m.role}: {m.content}\n"

    api_key = os.getenv("GEMINI_API_KEY")
    
    if not HAS_LLM or not api_key:
        # mock mode for testing without api key
        if len(request.messages) <= 1:
            context = ExtractedContext(intent="CLARIFY", role=None, seniority=None, skills=[])
        else:
            context = ExtractedContext(intent="RECOMMEND", role="Java Developer", seniority="mid", skills=["Java"])
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        Read this chat:
        {history_str}
        
        Find out if the intent is OUT_OF_SCOPE, CLARIFY, RECOMMEND, or COMPARE.
        Also get the role, seniority, skills, and test preferences.
        """
        
        try:
            resp = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=ExtractedContext
                )
            )
            context = ExtractedContext.model_validate_json(resp.text)
        except Exception as e:
            print("error calling gemini:", e)
            return ChatResponse(reply="Sorry, I didn't get that. Could you clarify?", recommendations=[], end_of_conversation=False)

    if context.intent == "OUT_OF_SCOPE":
        return ChatResponse(reply="I only help with SHL assessments.", recommendations=[], end_of_conversation=False)
        
    elif context.intent == "COMPARE" and len(context.comparison_tests) >= 2:
        tests_to_compare = []
        for t in CATALOG:
            for name in context.comparison_tests:
                if name.lower() in t["name"].lower():
                    tests_to_compare.append(t['name'])
        reply = "Here is the comparison for: " + " vs ".join(tests_to_compare)
        return ChatResponse(reply=reply, recommendations=[], end_of_conversation=False)
        
    elif context.intent == "RECOMMEND" or (context.role and (context.seniority or context.skills)):
        tests = retrieve_assessments(context)
        if len(tests) == 0:
            return ChatResponse(
                reply="I couldn't find any assessments matching this. Can we try something else?",
                recommendations=[],
                end_of_conversation=False
            )
            
        recs = []
        for t in tests:
            recs.append(Assessment(name=t["name"], url=t["url"], test_type=t["test_type"]))
            
        return ChatResponse(
            reply=f"Here are {len(recs)} tests I found.",
            recommendations=recs,
            end_of_conversation=True
        )
        
    else:
        missing = "seniority"
        if context.seniority:
            missing = "skills"
        return ChatResponse(
            reply=f"What {missing} do you need for the {context.role or 'role'}?",
            recommendations=[],
            end_of_conversation=False
        )
