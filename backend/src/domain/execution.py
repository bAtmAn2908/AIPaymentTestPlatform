from sqlalchemy.orm import Session
from datetime import datetime
from src.db.models import TestCase, TestLog, TestRun
from src.domain.simulation import PaymentSimulator
from src.core.exceptions import AppError
from src.core.logger import get_logger

logger = get_logger(__name__)

class TestExecutor:
    def __init__(self, db: Session):
        self.db = db
        # Instantiating simulation layer cleanly divorced from web inputs
        self.simulator = PaymentSimulator()

    def execute_suite(self, test_run_id: int):
        test_run = self.db.query(TestRun).filter(TestRun.id == test_run_id).first()
        if not test_run:
            logger.error(f"TestRun {test_run_id} not found to execute.")
            return

        test_run.status = "running"
        self.db.commit()

        cases = self.db.query(TestCase).all()
        total_latency = 0.0

        logger.info(f"Starting async execution for run_id={test_run_id} with {len(cases)} cases.", extra={"test_run_id": test_run_id})

        for case in cases:
            latency = 0.0
            error_type = None
            status = "fail"
            message = ""

            try:
                # Direct interaction with domain simulation
                result = self.simulator.process_payment(
                    amount=case.payload.get("amount", 100.0),
                    token=case.payload.get("token", "valid_token")
                )
                latency = result.get("latency_ms", 0.0)
                status = "pass" if result["status"] == case.expected_status else "fail"
                message = f"Simulated Success: Txn {result['transaction_id']}"
                
            except AppError as e:
                # Catch domain-specific simulated network/system errors cleanly
                latency = float(e.status_code) # Proxy to avoid losing data context when catching errors
                status = "pass" if "failed" == case.expected_status else "fail"
                error_type = e.code
                message = e.message
                logger.warning(f"Payment Simulator emitted expected edge-case: {error_type} - {message}", extra={"test_run_id": test_run_id})

            except Exception as e:
                status = "fail"
                error_type = "UNKNOWN_FATAL"
                message = str(e)
                logger.error(f"Engine threw unexpected unhandled fatal crash: {str(e)}", exc_info=True)

            total_latency += latency

            # Log execution result persistently
            log = TestLog(
                test_run_id=test_run.id,
                test_case_id=case.id,
                status=status,
                error_type=error_type,
                latency_ms=latency,
                message=message
            )
            self.db.add(log)
            self.db.commit()

        test_run.status = "completed"
        test_run.completed_at = datetime.utcnow()
        test_run.total_latency_ms = total_latency
        self.db.commit()
        logger.info(f"Test suite completed successfully.", extra={"test_run_id": test_run_id})
