from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import db
from app.routers import auth, resume, analyze, template, occupation
from app.routers import upload
from app.routers import ai_rewrite, ai_jobs
from app.routers import ai_verify, versions
from app.routers import health
from app.db.session import Base, engine
from app.observability.middleware import ObservabilityMiddleware
from app.observability.logging import configure_logging

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

app = FastAPI(title="Smart Resume Builder API")

logger = configure_logging(settings.LOG_LEVEL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ObservabilityMiddleware)

@app.get("/api/test")
def test_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    return {"message": "Authorized", "token": token}

@app.on_event("startup")
async def startup():
    logger.info("starting application", extra={"environment": settings.ENVIRONMENT, "service": settings.SERVICE_NAME})
    db.connect()
    # Ensure SQLAlchemy models are created in dev (production should use Alembic)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass

@app.on_event("shutdown")
async def shutdown():
    db.disconnect()

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(resume.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["ATS"])
app.include_router(template.router, prefix="/api/templates", tags=["Templates"])
app.include_router(occupation.router, prefix="/api/occupations", tags=["Occupations"])
app.include_router(upload.router, prefix="/api/resume", tags=["Upload"])
app.include_router(ai_rewrite.router)
app.include_router(ai_jobs.router)
app.include_router(ai_verify.router)
app.include_router(versions.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Smart Resume Builder API is running"}
