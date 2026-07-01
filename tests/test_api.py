from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_agent_service
from app.models.schemas import ChatResponse, Recommendation

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

class MockAgentService:
    def generate_response(self, request):
        return ChatResponse(
            reply="This is a mock reply",
            recommendations=[
                Recommendation(
                    name="Mock Test",
                    url="https://www.shl.com/mock",
                    test_type="K"
                )
            ],
            end_of_conversation=True
        )

def override_get_agent_service():
    return MockAgentService()

app.dependency_overrides[get_agent_service] = override_get_agent_service

def test_chat_endpoint():
    payload = {
        "messages": [
            {"role": "user", "content": "I need a test for a developer."}
        ]
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "recommendations" in data
    assert "end_of_conversation" in data
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["name"] == "Mock Test"
