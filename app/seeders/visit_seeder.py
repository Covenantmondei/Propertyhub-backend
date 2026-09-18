from sqlalchemy.orm import Session
from app.auth.models import User, UserRole
from app.property.models import (
    UserProperty, VisitRequest, VisitStatus, VisitType,
    AgentReview, Favorite, PropertyReservation
)
from datetime import datetime, timedelta

def seed_visits(db: Session):
    """Seed Favorites, VisitRequests, PropertyReservations, and AgentReviews."""
    print("Seeding visit requests, favorites, and agent reviews...")

    buyers = db.query(User).filter(User.role == UserRole.BUYER.value).all()
    properties = db.query(UserProperty).all()

    if not buyers or not properties:
        print(" -> Error: Buyers and Properties must exist before seeding visits. Run seed-users and seed-properties first!")
        return

    # 1. Seed Favorites
    fav_count = 0
    for buyer in buyers[:5]:
        for prop in properties[:3]:
            existing_fav = db.query(Favorite).filter(
                Favorite.user_id == buyer.id,
                Favorite.property_id == prop.id
            ).first()
            if not existing_fav:
                fav = Favorite(
                    user_id=buyer.id,
                    property_id=prop.id,
                    created_at=datetime.utcnow() - timedelta(days=2)
                )
                db.add(fav)
                fav_count += 1
    print(f" -> Created {fav_count} Favorites.")

    # 2. Seed Visit Requests
    visit_count = 0
    sample_buyer = buyers[0]
    sample_buyer_2 = buyers[1]

    for index, prop in enumerate(properties[:4]):
        # Completed visit
        visit_1 = VisitRequest(
            property_id=prop.id,
            buyer_id=sample_buyer.id,
            agent_id=prop.agent_id,
            visit_type=VisitType.PHYSICAL.value,
            status=VisitStatus.COMPLETED.value,
            preferred_date=datetime.utcnow() - timedelta(days=5),
            preferred_time_start="10:00",
            preferred_time_end="11:00",
            buyer_note="Would love to inspect the master bedroom and backyard.",
            confirmed_date=datetime.utcnow() - timedelta(days=5),
            confirmed_time_start="10:00",
            confirmed_time_end="11:00",
            completed_at=datetime.utcnow() - timedelta(days=5),
            is_buyer_interested=True
        )
        db.add(visit_1)
        db.flush()
        visit_count += 1

        # Add Agent Review for completed visit
        existing_review = db.query(AgentReview).filter(AgentReview.visit_request_id == visit_1.id).first()
        if not existing_review:
            review = AgentReview(
                agent_id=prop.agent_id,
                buyer_id=sample_buyer.id,
                visit_request_id=visit_1.id,
                property_id=prop.id,
                rating=5,
                review_text="Punctual, professional, and knew every detail about the property history!",
                communication_rating=5,
                professionalism_rating=5,
                knowledge_rating=5,
                responsiveness_rating=5,
                would_recommend=True
            )
            db.add(review)

        # Pending visit for another buyer
        visit_2 = VisitRequest(
            property_id=prop.id,
            buyer_id=sample_buyer_2.id,
            agent_id=prop.agent_id,
            visit_type=VisitType.VIRTUAL.value,
            status=VisitStatus.PENDING.value,
            preferred_date=datetime.utcnow() + timedelta(days=2),
            preferred_time_start="14:00",
            preferred_time_end="15:00",
            buyer_note="Interested in a virtual tour via Zoom."
        )
        db.add(visit_2)
        visit_count += 1

    # 3. Seed Property Reservation
    res_prop = properties[0]
    existing_res = db.query(PropertyReservation).filter(PropertyReservation.property_id == res_prop.id).first()
    if not existing_res:
        reservation = PropertyReservation(
            property_id=res_prop.id,
            buyer_id=sample_buyer.id,
            agent_id=res_prop.agent_id,
            status="confirmed",
            reservation_date=datetime.utcnow() - timedelta(days=1),
            expiry_date=datetime.utcnow() + timedelta(days=6),
            buyer_note="Holding deposit intent submitted.",
            is_buyer_interested=True
        )
        db.add(reservation)
        print(f" -> Created sample PropertyReservation for property ID {res_prop.id}.")

    db.commit()
    print(f"Visit seeding completed ({visit_count} visit requests & reviews created)!")

