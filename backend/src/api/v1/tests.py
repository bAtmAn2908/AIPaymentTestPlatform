from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.db.session import get_db
from src.db.models import TestCase, TestRun
from src.domain.analytics import AnomalyDetector
from src.worker.tasks import execute_test_suite_task

router = APIRouter(prefix="/api/tests", tags=["Tests"])

class TestCaseCreate(BaseModel):
    name: str
    payload: dict
    expected_status: str

@router.post("/cases")
def create_test_case(case: TestCaseCreate, db: Session = Depends(get_db)):
    db_case = TestCase(name=case.name, payload=case.payload, expected_status=case.expected_status)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get("/cases")
def list_test_cases(db: Session = Depends(get_db)):
    return db.query(TestCase).all()

@router.post("/runs")
def trigger_test_run(db: Session = Depends(get_db)):
    # Persist the start intent quickly via synchronous REST
    test_run = TestRun(status="pending")
    db.add(test_run)
    db.commit()
    db.refresh(test_run)
    
    # Hand execution block off cleanly to Celery backend worker
    execute_test_suite_task.delay(test_run.id)
    
    return {"message": "Test run automatically queued onto async broker", "test_run_id": test_run.id}

@router.get("/runs")
def list_test_runs(db: Session = Depends(get_db)):
    return db.query(TestRun).order_by(TestRun.id.desc()).all()

@router.get("/insights")
def get_insights(db: Session = Depends(get_db)):
    # Dependency injected analytical controller
    detector = AnomalyDetector(db)
    return detector.get_insights()
