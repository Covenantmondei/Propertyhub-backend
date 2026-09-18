import json
from sqlalchemy.orm import Session
from app.auth.models import User, UserRole
from app.property.models import UserProperty, PropertyImage, ApprovalStatus
from datetime import datetime

SAMPLE_PROPERTIES = [
    {
        "title": "Modern Luxury Villa in Sunset Hills",
        "description": "Exquisite 4-bedroom villa featuring floor-to-ceiling glass windows, a private infinity pool, chef's kitchen, and panoramic ocean and sunset views.",
        "property_type": "villa",
        "listing_type": "sale",
        "price": 2450000.0,
        "bedrooms": 4,
        "bathrooms": 5,
        "area_sqft": 4800.0,
        "address": "742 Evergreen Terrace",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "year_built": 2022,
        "parking_spaces": 3,
        "amenities": json.dumps(["Swimming Pool", "Gym", "Smart Home System", "Solar Panels", "Wine Cellar"]),
        "images": [
            ("https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800", True),
            ("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800", False),
            ("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800", False)
        ]
    },
    {
        "title": "Downtown High-Rise Penthouse",
        "description": "Top-floor penthouse in the heart of downtown with private rooftop terrace, concierge services, floor heating, and designer finishes throughout.",
        "property_type": "apartment",
        "listing_type": "sale",
        "price": 1850000.0,
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 2900.0,
        "address": "100 Grand Avenue, Unit 45A",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "year_built": 2023,
        "parking_spaces": 2,
        "amenities": json.dumps(["Rooftop Deck", "Concierge", "Elevator", "Central AC", "Doorman"]),
        "images": [
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800", True),
            ("https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800", False),
            ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800", False)
        ]
    },
    {
        "title": "Charming Waterfront Cottage",
        "description": "Peaceful lakefront cottage with private dock, wood-burning fireplace, wraparound porch, and lush surrounding nature.",
        "property_type": "house",
        "listing_type": "sale",
        "price": 725000.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 2100.0,
        "address": "452 Lakeview Drive",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "year_built": 2018,
        "parking_spaces": 2,
        "amenities": json.dumps(["Waterfront", "Private Dock", "Fireplace", "Garden", "Deck"]),
        "images": [
            ("https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800", True),
            ("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800", False)
        ]
    },
    {
        "title": "Modern Urban Condo in South Beach",
        "description": "Sleek 2-bedroom condo located steps from the beach, vibrant nightlife, gourmet dining, and tropical palm gardens.",
        "property_type": "condo",
        "listing_type": "rent",
        "price": 4500.0,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1400.0,
        "address": "888 Ocean Drive",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33139",
        "year_built": 2021,
        "parking_spaces": 1,
        "amenities": json.dumps(["Beach Access", "Pool", "Fitness Center", "Valet Parking", "Balcony"]),
        "images": [
            ("https://images.unsplash.com/photo-1567496898669-ee935f5f647a?w=800", True),
            ("https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800", False)
        ]
    },
    {
        "title": "Spacious Suburban Family Home",
        "description": "Beautiful 5-bedroom traditional family residence with large backyard, open-concept kitchen, and proximity to top-rated schools.",
        "property_type": "house",
        "listing_type": "sale",
        "price": 985000.0,
        "bedrooms": 5,
        "bathrooms": 4,
        "area_sqft": 3600.0,
        "address": "120 Oakridge Lane",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "year_built": 2019,
        "parking_spaces": 2,
        "amenities": json.dumps(["Backyard", "Garage", "Hardwood Floors", "Walk-in Closet", "Laundry Room"]),
        "images": [
            ("https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800", True),
            ("https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800", False)
        ]
    },
    {
        "title": "Contemporary Loft in Arts District",
        "description": "Industrial chic loft featuring high ceilings, exposed brick walls, custom ironwork, and skylights.",
        "property_type": "apartment",
        "listing_type": "rent",
        "price": 3200.0,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqft": 1100.0,
        "address": "550 Factory Street, Loft 3B",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60601",
        "year_built": 2020,
        "parking_spaces": 1,
        "amenities": json.dumps(["Exposed Brick", "High Ceilings", "Pet Friendly", "In-unit Laundry"]),
        "images": [
            ("https://images.unsplash.com/photo-1502672016976-663884d6b637?w=800", True),
            ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800", False)
        ]
    },
    {
        "title": "Scenic Mountain View Estate",
        "description": "Exclusive mountain estate nestled on 5 acres with heated pool, outdoor kitchen, fire pit, and majestic alpine scenery.",
        "property_type": "villa",
        "listing_type": "sale",
        "price": 3100000.0,
        "bedrooms": 6,
        "bathrooms": 6,
        "area_sqft": 6200.0,
        "address": "1500 Alpine Way",
        "city": "Denver",
        "state": "CO",
        "zip_code": "80202",
        "year_built": 2021,
        "parking_spaces": 4,
        "amenities": json.dumps(["Mountain View", "Heated Pool", "Outdoor Kitchen", "Fire Pit", "Security System"]),
        "images": [
            ("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800", True),
            ("https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800", False)
        ]
    },
    {
        "title": "Prime Commercial Retail Space",
        "description": "High-traffic street frontage retail space ideal for boutique store, cafe, or high-end showroom.",
        "property_type": "land",
        "listing_type": "rent",
        "price": 6500.0,
        "bedrooms": 0,
        "bathrooms": 2,
        "area_sqft": 2500.0,
        "address": "410 Main Commercial Boulevard",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78702",
        "year_built": 2017,
        "parking_spaces": 5,
        "amenities": json.dumps(["High Traffic", "Street Frontage", "Storage Room", "HVAC"]),
        "images": [
            ("https://images.unsplash.com/photo-1497366216548-37526070297c?w=800", True)
        ]
    }
]

def seed_properties(db: Session):
    """Seed properties assigned to existing agents."""
    print("Seeding properties...")
    
    agents = db.query(User).filter(User.role == UserRole.AGENT.value).all()
    if not agents:
        print(" -> Error: No agents found. Please run seed-users first!")
        return

    created_count = 0
    for index, item in enumerate(SAMPLE_PROPERTIES):
        agent = agents[index % len(agents)]
        
        # Avoid duplicate titles for idempotency
        existing = db.query(UserProperty).filter(UserProperty.title == item["title"]).first()
        if existing:
            continue
            
        prop = UserProperty(
            agent_id=agent.id,
            title=item["title"],
            description=item["description"],
            property_type=item["property_type"],
            listing_type=item["listing_type"],
            price=item["price"],
            bedrooms=item["bedrooms"],
            bathrooms=item["bathrooms"],
            area_sqft=item["area_sqft"],
            address=item["address"],
            city=item["city"],
            state=item["state"],
            zip_code=item["zip_code"],
            year_built=item["year_built"],
            parking_spaces=item["parking_spaces"],
            amenities=item["amenities"],
            is_available=True,
            is_approved=True,
            approval_status=ApprovalStatus.APPROVED.value,
            created_at=datetime.utcnow()
        )
        db.add(prop)
        db.flush()

        for img_url, is_primary in item["images"]:
            p_img = PropertyImage(
                property_id=prop.id,
                image_url=img_url,
                is_primary=is_primary
            )
            db.add(p_img)
            
        created_count += 1
        print(f" -> Created property: '{prop.title}' (Agent: {agent.email})")

    db.commit()
    print(f"Property seeding completed ({created_count} new properties created)!")

