import pytest
from src.domain.execution import TestExecutor
from src.db.models import TestCase, TestRun

def test_execution_handles_errors_gracefully(mocker):
    # Mock database repository behavior
    mock_db = mocker.MagicMock()
    
    mock_run = TestRun(id=1, status="pending")
    mock_db.query().filter().first.return_value = mock_run
    
    mock_case = TestCase(id=1, payload={"amount": 100, "token": "invalid_token"}, expected_status="success")
    mock_db.query().all.return_value = [mock_case]
    
    # Execute
    executor = TestExecutor(db=mock_db)
    executor.execute_suite(1)
    
    # Asserts
    assert mock_run.status == "completed"
    assert mock_db.add.called
    
    # Verify execution correctly mapped the Simulation exception to a structured DB Log
    added_log = mock_db.add.call_args[0][0]
    assert added_log.status == "fail"
    assert added_log.error_type == "INVALID_TOKEN"
