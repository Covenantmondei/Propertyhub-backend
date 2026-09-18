from sqlalchemy.orm import Session
from app.auth.models import User, AgentProfile, ActivityLog, TokenBlacklist
from app.property.models import (
    UserProperty, PropertyImage, Favorite, VisitRequest,
    PropertyReservation, AgentReview
)

def clear_database(db: Session):
    """Deletes all seeded data in reverse foreign key order."""
    print("Clearing database records...")
    
    deleted_reviews = db.query(AgentReview).delete()
    deleted_reservations = db.query(PropertyReservation).delete()
    deleted_visits = db.query(VisitRequest).delete()
    deleted_favorites = db.query(Favorite).delete()
    deleted_images = db.query(PropertyImage).delete()
    deleted_properties = db.query(UserProperty).delete()
    deleted_logs = db.query(ActivityLog).delete()
    deleted_profiles = db.query(AgentProfile).delete()
    deleted_users = db.query(User).delete()
    
    db.commit()
    print(f"Database cleared: {deleted_users} users, {deleted_profiles} agent profiles, {deleted_properties} properties, {deleted_visits} visits, {deleted_reviews} reviews deleted.")

