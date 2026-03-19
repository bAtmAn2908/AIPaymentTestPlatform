class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

class SimulationTimeoutError(AppError):
    def __init__(self, message="Payment simulation timed out"):
        super().__init__(message, code="TIMEOUT_ERROR", status_code=504)

class PaymentProcessingError(AppError):
    def __init__(self, message="Payment processing failed", code="PROCESSING_ERROR"):
        super().__init__(message, code=code, status_code=422)

class DuplicateTransactionError(AppError):
    def __init__(self, message="Duplicate transaction detected over network"):
        super().__init__(message, code="DUPLICATE_TRANSACTION", status_code=409)

class PartialProcessingError(AppError):
    def __init__(self, message="Transaction partially failed downstream"):
        super().__init__(message, code="PARTIAL_FAILURE", status_code=207)

class ResourceNotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, code="NOT_FOUND", status_code=404)
