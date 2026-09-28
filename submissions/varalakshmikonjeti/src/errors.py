class PackManagerError(Exception):
    """Base exception for Pack Manager errors."""


class ValidationError(PackManagerError):
    """Raised when a verification request is invalid."""


class ImageProcessingError(PackManagerError):
    """Raised when the submitted image cannot be processed."""


class ModelVerificationError(PackManagerError):
    """Raised when model/API verification fails."""


class TenantIsolationError(PackManagerError):
    """Raised when a cross-tenant access attempt is detected."""


class RecordNotFoundError(PackManagerError):
    """Raised when a requested verification record does not exist."""