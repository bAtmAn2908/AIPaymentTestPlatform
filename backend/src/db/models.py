from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    payload = Column(JSON)
    expected_status = Column(String)

class TestRun(Base):
    __tablename__ = "test_runs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    total_latency_ms = Column(Float, nullable=True)

class TestLog(Base):
    __tablename__ = "test_logs"
    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    test_case_id = Column(Integer, ForeignKey("test_cases.id"))
    status = Column(String)  # 'pass' or 'fail'
    error_type = Column(String, nullable=True) # e.g., TIMEOUT, FLAKY, DUPLICATE
    latency_ms = Column(Float)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
