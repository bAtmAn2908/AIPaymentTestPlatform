from celery import Celery
from src.core.config import settings
from src.db.session import SessionLocal
from src.domain.execution import TestExecutor
from src.core.logger import get_logger

logger = get_logger(__name__)

celery_app = Celery(
    "payment_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1 # Enforce fair queue processing
)

@celery_app.task
def execute_test_suite_task(suite_id: int):
    logger.info(f"Celery received Background Task -> Execute Suite {suite_id}", extra={"test_run_id": suite_id})
    db = SessionLocal()
    try:
        executor = TestExecutor(db)
        executor.execute_suite(suite_id)
        return {"status": "completed", "suite_id": suite_id}
    except Exception as e:
        logger.error(f"Fatal Celery Queue Exception for Suite {suite_id}: {str(e)}", exc_info=True)
        return {"status": "failed", "suite_id": suite_id, "error": str(e)}
    finally:
        db.close()
