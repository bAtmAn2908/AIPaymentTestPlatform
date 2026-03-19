from sqlalchemy.orm import Session
from src.db.models import TestLog
from sqlalchemy import func, case
from src.core.logger import get_logger

logger = get_logger(__name__)

class AnomalyDetector:
    def __init__(self, db: Session):
        self.db = db

    def get_insights(self):
        logger.info("Executing AI anomaly detection heuristics on historical test logs.")
        
        # Aggregate structural statistics natively via SQL
        results = self.db.query(
            TestLog.test_case_id,
            func.count(TestLog.id).label('total_runs'),
            func.sum(case((TestLog.status == 'fail', 1), else_=0)).label('failures'),
            func.avg(TestLog.latency_ms).label('avg_latency'),
            func.max(TestLog.error_type).label('common_error') 
        ).group_by(TestLog.test_case_id).all()

        insights = []
        for r in results:
            fail_rate = r.failures / r.total_runs if r.total_runs > 0 else 0
            
            # Flaky tests pattern
            if 0 < fail_rate < 1.0:
                insights.append({
                    "test_case_id": r.test_case_id,
                    "type": "FLAKY_TEST",
                    "description": f"Test is inconsistently breaking, failing {fail_rate*100:.1f}% of the time.",
                    "severity": "high" if fail_rate >= 0.3 else "medium"
                })
            
            # Consistent failure pattern
            if fail_rate == 1.0:
                insights.append({
                    "test_case_id": r.test_case_id,
                    "type": "CONSISTENT_FAILURE",
                    "description": f"Test fails 100% of the time seamlessly. (Primary Context: {r.common_error})",
                    "severity": "critical"
                })
            
            # High latency anomalous pattern 
            if r.avg_latency and r.avg_latency > 800:
                insights.append({
                    "test_case_id": r.test_case_id,
                    "type": "HIGH_LATENCY",
                    "description": f"Abnormally high structural execution latency detected: {r.avg_latency:.1f}ms",
                    "severity": "high"
                })

        return insights
