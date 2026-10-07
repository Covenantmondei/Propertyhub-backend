import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, property, admin, chat, visits, kyc, reviews
from app.auth.models import User, AgentProfile, ActivityLog
from app.property.models import UserProperty, PropertyImage, Favorite, VisitRequest, PropertyReservation, AgentReview
from app.chat.models import Conversation, Message, Notification
from app.keep_alive import keep_alive_db_worker
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch database keep-alive worker (pings database every 5 mins)
    keep_alive_task = asyncio.create_task(keep_alive_db_worker(interval_seconds=300))
    yield
    # Shutdown: Cancel worker task gracefully
    keep_alive_task.cancel()
    try:
        await keep_alive_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Real Estate API",
    description="A comprehensive real estate management system",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    'http://localhost:5500',
    'http://localhost:5501',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5501',
    'https://mypropertyhub.vercel.app',
    'https://mypropertyhub.dev',
    'https://www.mypropertyhub.dev'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_origin_regex = r"https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(user.router)
app.include_router(property.router)
app.include_router(admin.router)
app.include_router(chat.router)
app.include_router(visits.router)
app.include_router(kyc.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {
        'message': 'Welcome to the PropertyHub API',
        'version': '1.0.0',
        'docs': '/docs',
        'redoc': '/redoc'
    }
