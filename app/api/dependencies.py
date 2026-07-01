import os
from app.services.catalog import load_catalog
from app.services.agent import AgentService

# Dependency singleton
CATALOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "catalog.json")

catalog_data = load_catalog(CATALOG_PATH)
agent_service = AgentService(catalog_data=catalog_data)

def get_agent_service() -> AgentService:
    return agent_service
