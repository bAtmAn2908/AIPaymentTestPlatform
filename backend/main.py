from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.db.session import engine, SessionLocal
from src.db.models import Base, TestCase
from src.api.v1 import tests
from src.core.handlers import add_exception_handlers
from src.core.logger import get_logger

logger = get_logger(__name__)

# Initialize DB Tables
logger.info("Initializing Database schema")
Base.metadata.create_all(bind=engine)

# Seed initial enhanced test cases if database is empty
db = SessionLocal()
try:
    if db.query(TestCase).count() == 0:
        logger.info("Seeding database with enhanced payment scenarios.")
        seed_cases = [
            TestCase(name="Standard Credit Auth", payload={"amount": 100.0, "token": "valid_token"}, expected_status="success"),
            TestCase(name="High Volume Stress", payload={"amount": 5000.0, "token": "valid_token"}, expected_status="success"),
            TestCase(name="Expired Token Drop", payload={"amount": 50.0, "token": "invalid_token"}, expected_status="failed"),
            TestCase(name="Network Spiky Drop", payload={"amount": 150.0, "token": "valid_token"}, expected_status="success"),
            TestCase(name="Fraud Check Wait", payload={"amount": 25000.0, "token": "valid_token"}, expected_status="success"),
            TestCase(name="Duplicate Validation", payload={"amount": 25.0, "token": "duplicate_token"}, expected_status="success"),
        ]
        db.add_all(seed_cases)
        db.commit()
finally:
    db.close()

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register central error handlers globally
add_exception_handlers(app)

@app.get("/health")
def health_check():
    return {"status": "ok", "architecture": "domain-driven"}

# Register nested modular routes
app.include_router(tests.router)
