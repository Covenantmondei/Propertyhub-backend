from sqlalchemy.orm import Session
from app.auth.models import User, AgentProfile, UserRole, ApprovalStatus, KYCStatus
from app.auth.hash import Hash
from datetime import datetime

COMMON_PASSWORD = "Test1234!"

AGENT_DATA = [
    {
        "first_name": "Sarah",
        "last_name": "Jenkins",
        "username": "agent1",
        "email": "agent1@propertyhub.com",
        "company": "Apex Real Estate",
        "phone": "+1 (555) 123-4567",
        "bio": "Specializing in luxury residential properties with over 8 years of market expertise.",
        "experience": 8,
        "rating": 4.9,
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400"
    },
    {
        "first_name": "Michael",
        "last_name": "Chen",
        "username": "agent2",
        "email": "agent2@propertyhub.com",
        "company": "Bayview Properties",
        "phone": "+1 (555) 234-5678",
        "bio": "Dedicated commercial and urban apartment specialist in prime downtown locations.",
        "experience": 6,
        "rating": 4.8,
        "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400"
    },
    {
        "first_name": "Elena",
        "last_name": "Rostova",
        "username": "agent3",
        "email": "agent3@propertyhub.com",
        "company": "Grand Horizon Realty",
        "phone": "+1 (555) 345-6789",
        "bio": "Passionate about helping families find their dream suburban homes and estates.",
        "experience": 10,
        "rating": 5.0,
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400"
    },
    {
        "first_name": "David",
        "last_name": "Miller",
        "username": "agent4",
        "email": "agent4@propertyhub.com",
        "company": "Coastal Living Realty",
        "phone": "+1 (555) 456-7890",
        "bio": "Waterfront and beach house property consultant with deep local insights.",
        "experience": 5,
        "rating": 4.7,
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"
    },
    {
        "first_name": "Rachel",
        "last_name": "Adams",
        "username": "agent5",
        "email": "agent5@propertyhub.com",
        "company": "Metro Realty Group",
        "phone": "+1 (555) 567-8901",
        "bio": "Expert in modern condos, townhouses, and investment properties.",
        "experience": 7,
        "rating": 4.9,
        "avatar": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400"
    }
]

BUYER_DATA = [
    ("John", "Doe", "buyer1", "buyer1@propertyhub.com"),
    ("Jane", "Smith", "buyer2", "buyer2@propertyhub.com"),
    ("Robert", "Johnson", "buyer3", "buyer3@propertyhub.com"),
    ("Emily", "Davis", "buyer4", "buyer4@propertyhub.com"),
    ("Carlos", "Gomez", "buyer5", "buyer5@propertyhub.com"),
    ("Sophia", "Wilson", "buyer6", "buyer6@propertyhub.com"),
    ("Liam", "Taylor", "buyer7", "buyer7@propertyhub.com"),
    ("Olivia", "Anderson", "buyer8", "buyer8@propertyhub.com"),
    ("Ethan", "Thomas", "buyer9", "buyer9@propertyhub.com"),
    ("Ava", "Jackson", "buyer10", "buyer10@propertyhub.com"),
]

def seed_users(db: Session):
    """Seed Admin, 5 Agents with profiles, and 10 Buyers into the database."""
    print("Seeding users...")
    hashed_password = Hash.bcrypt(COMMON_PASSWORD)

    # 1. Seed Admin
    admin = db.query(User).filter(User.email == "admin@propertyhub.com").first()
    if not admin:
        admin = User(
            first_name="Admin",
            last_name="User",
            username="admin",
            email="admin@propertyhub.com",
            password=hashed_password,
            role=UserRole.ADMIN.value,
            is_verified=True,
            is_approved=True,
            approval_status=ApprovalStatus.APPROVED.value,
            created_at=datetime.utcnow()
        )
        db.add(admin)
        print(" -> Created Admin: admin@propertyhub.com (Password: Test1234!)")

    # 2. Seed Agents + Agent Profiles
    for data in AGENT_DATA:
        agent_user = db.query(User).filter(User.email == data["email"]).first()
        if not agent_user:
            agent_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                username=data["username"],
                email=data["email"],
                password=hashed_password,
                role=UserRole.AGENT.value,
                is_verified=True,
                is_approved=True,
                approval_status=ApprovalStatus.APPROVED.value,
                kyc_status=KYCStatus.VERIFIED.value,
                kyc_verified_at=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            db.add(agent_user)
            db.flush()

            profile = AgentProfile(
                user_id=agent_user.id,
                company=data["company"],
                phone_number=data["phone"],
                bio=data["bio"],
                years_experience=data["experience"],
                rating=data["rating"],
                total_ratings=12,
                profile_picture=data["avatar"],
                id_type="National ID",
                id_number="ID-9928172"
            )
            db.add(profile)
            print(f" -> Created Agent: {data['email']} (Password: Test1234!)")

    # 3. Seed Buyers
    for first_name, last_name, username, email in BUYER_DATA:
        buyer = db.query(User).filter(User.email == email).first()
        if not buyer:
            buyer = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashed_password,
                role=UserRole.BUYER.value,
                is_verified=True,
                is_approved=True,
                approval_status=ApprovalStatus.APPROVED.value,
                created_at=datetime.utcnow()
            )
            db.add(buyer)
            print(f" -> Created Buyer: {email} (Password: Test1234!)")

    db.commit()
    print("User seeding completed!")

