import random
import time
import uuid
from src.core.exceptions import (
    SimulationTimeoutError, 
    PaymentProcessingError, 
    DuplicateTransactionError,
    PartialProcessingError
)
from src.core.logger import get_logger

logger = get_logger(__name__)

class PaymentSimulator:
    def __init__(self, failure_rate=0.1, timeout_rate=0.05, duplicate_rate=0.05, partial_rate=0.05):
        self.failure_rate = failure_rate
        self.timeout_rate = timeout_rate
        self.duplicate_rate = duplicate_rate
        self.partial_rate = partial_rate
        self.processed_tokens = set()

    def process_payment(self, amount: float, token: str):
        # 1. High Latency / Timeout Simulation
        if random.random() < self.timeout_rate:
            time.sleep(1.5) # Simulate long hang
            logger.warning("Simulation blocked, timing out request.")
            raise SimulationTimeoutError()
            
        # Simulate realistic latency distribution heavily focused on 50-200ms
        latency = random.paretovariate(2) * 50
        latency = min(latency, 1200) # Cap latency to 1.2s max
        
        # Artificial high-latency edge cases
        if random.random() < 0.05:
            latency = random.uniform(800, 1200)
            
        time.sleep(latency / 1000.0)

        # 2. Prevent Duplicate Transactions natively
        if token in self.processed_tokens and random.random() < self.duplicate_rate:
            raise DuplicateTransactionError()
        self.processed_tokens.add(token)

        # 3. Intermittent Failure (Network drop / downstream 500)
        if random.random() < self.failure_rate:
            raise PaymentProcessingError(message="Random network interruption", code="NETWORK_DROP")
            
        # Hard fail on explicit bad tokens
        if token == "invalid_token":
            raise PaymentProcessingError(message="Token is expired or invalid", code="INVALID_TOKEN")
            
        # 4. Partial Processing (e.g., Authorized but not captured)
        if random.random() < self.partial_rate:
            raise PartialProcessingError()

        return {
            "status": "success", 
            "transaction_id": f"txn_{uuid.uuid4().hex[:8]}", 
            "latency_ms": round(latency, 2)
        }
