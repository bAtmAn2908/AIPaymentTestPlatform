import pytest
from src.domain.simulation import PaymentSimulator
from src.core.exceptions import (
    SimulationTimeoutError,
    PaymentProcessingError,
    DuplicateTransactionError
)

def test_standard_payment_success():
    simulator = PaymentSimulator(failure_rate=0, timeout_rate=0, duplicate_rate=0, partial_rate=0)
    result = simulator.process_payment(100, "valid_token")
    assert result["status"] == "success"
    assert "transaction_id" in result
    assert "latency_ms" in result

def test_invalid_token_hard_failure():
    simulator = PaymentSimulator()
    with pytest.raises(PaymentProcessingError) as exc_info:
        simulator.process_payment(100, "invalid_token")
    assert exc_info.value.code == "INVALID_TOKEN"

def test_timeout_simulation(mocker):
    # Force timeout probability to 1.0 (100%)
    simulator = PaymentSimulator(failure_rate=0, timeout_rate=1.0, duplicate_rate=0, partial_rate=0)
    # Mock sleep to prevent hanging unit tests
    mocker.patch('time.sleep', return_value=None)
    with pytest.raises(SimulationTimeoutError) as exc_info:
        simulator.process_payment(100, "valid_token")
    assert exc_info.value.code == "TIMEOUT_ERROR"

def test_duplicate_transaction(mocker):
    simulator = PaymentSimulator(failure_rate=0, timeout_rate=0, duplicate_rate=1.0, partial_rate=0)
    mocker.patch('time.sleep', return_value=None)
    
    # First pass
    simulator.process_payment(100, "token_123")
    
    # Second duplicate pass
    with pytest.raises(DuplicateTransactionError) as exc_info:
        simulator.process_payment(100, "token_123")
    assert exc_info.value.code == "DUPLICATE_TRANSACTION"
