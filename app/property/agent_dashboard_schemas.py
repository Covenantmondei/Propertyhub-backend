from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AgentSummaryInfo(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    kyc_status: Optional[str] = "unverified"
    is_approved: bool = True
    approval_status: Optional[str] = "approved"

    class Config:
        from_attributes = True


class AgentDashboardMetrics(BaseModel):
    total_listings: int = 0
    approved_listings: int = 0
    pending_listings: int = 0
    pending_visits: int = 0
    completed_visits: int = 0
    total_favorites: int = 0
    average_rating: float = 5.0
    total_ratings: int = 0


class RecentVisitSummary(BaseModel):
    id: int
    property_id: int
    property_title: str
    buyer_name: str
    buyer_email: str
    visit_type: str
    status: str
    preferred_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class RecentPropertySummary(BaseModel):
    id: int
    title: str
    property_type: str
    listing_type: str
    price: float
    is_available: bool
    is_approved: bool
    approval_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentDashboardResponse(BaseModel):
    agent_info: AgentSummaryInfo
    metrics: AgentDashboardMetrics
    recent_visit_requests: List[RecentVisitSummary] = []
    recent_properties: List[RecentPropertySummary] = []

    class Config:
        from_attributes = True

