import json
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.agent import AgentService
from app.models.schemas import ChatRequest, Message

# Ground Truth Dataset
# List of tuples: (Query String, Expected Set of Test Names)
TEST_CASES = [
    (
        "I need an assessment for a Java developer",
        {
            "Core Java (Advanced Level) (New)",
            "Spring (New)",
            "RESTful Web Services (New)"
        }
    ),
    (
        "What about something for customer service phone calls?",
        {
            "Customer Service Phone Simulation",
            "Contact Center Call Simulation (New)",
            "Entry Level Customer Serv - Retail & Contact Center"
        }
    ),
    (
        "I need to test AWS and Docker skills",
        {
            "Amazon Web Services (AWS) Development (New)",
            "Docker (New)"
        }
    ),
    (
        "Do you have a general personality test?",
        {
            "Occupational Personality Questionnaire OPQ32r",
            "Dependability and Safety Instrument (DSI)" # Being generous, allowing multiple personality tests
        }
    ),
    (
        "Assess basic Microsoft Office skills like Word and Excel",
        {
            "MS Word (New)",
            "MS Excel (New)",
            "Microsoft Word 365 (New)",
            "Microsoft Excel 365 (New)",
            "Microsoft Word 365 - Essentials (New)"
        }
    )
]

def load_catalog():
    catalog_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'catalog.json')
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_evaluation():
    print("Starting Precision & Recall Evaluation...\n")
    from app.core.config import settings
    if settings.GEMINI_API_KEY:
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
    else:
        print("WARNING: GEMINI_API_KEY is not set in settings!")
        
    catalog_data = load_catalog()
    agent = AgentService(catalog_data)
    
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    for i, (query, expected_set) in enumerate(TEST_CASES):
        print(f"--- Test Case {i+1} ---")
        print(f"Query: {query}")
        print(f"Expected: {expected_set}")
        
        request = ChatRequest(messages=[Message(role="user", content=query)])
        
        try:
            response = agent.generate_response(request)
            recommended_set = {rec.name for rec in response.recommendations}
            print(f"Recommended: {recommended_set}")
            
            # Allow for some flexibility:
            # We consider an expected test as "hit" if the recommended test name is in the expected set.
            # We might have cases where the LLM recommends tests we didn't strictly expect.
            
            tp = len(recommended_set.intersection(expected_set))
            fp = len(recommended_set - expected_set)
            fn = len(expected_set - recommended_set)
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
            
            print(f"Metrics: TP={tp}, FP={fp}, FN={fn}\n")
        except Exception as e:
            print(f"ERROR processing query: {e}\n")
            
    # Calculate overall metrics
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    
    print("=========================")
    print("      FINAL RESULTS      ")
    print("=========================")
    print(f"Total True Positives (TP): {total_tp}")
    print(f"Total False Positives (FP): {total_fp}")
    print(f"Total False Negatives (FN): {total_fn}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")

if __name__ == '__main__':
    run_evaluation()
