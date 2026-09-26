from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import User
from app.auth.oauth2 import get_current_user
from app.property import property
from app.property.agent_dashboard_schemas import AgentDashboardResponse

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)


@router.get("/dashboard", response_model=AgentDashboardResponse)
def get_agent_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint to retrieve dashboard metrics and recent leads/listings for the authenticated agent.
    """
    return property.get_agent_dashboard_stats(db, current_user.id)

