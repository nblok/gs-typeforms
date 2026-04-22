from common.domain.exception.domain_exception import DomainException


class TypeformsDomainException(DomainException):
    pass


class ResponseNotFoundError(TypeformsDomainException):
    pass


class FormNotFoundError(TypeformsDomainException):
    pass


class FieldConfigValidationError(TypeformsDomainException):
    """Raised when a response answer violates a field's config constraints."""


class FormValidationError(TypeformsDomainException):
    pass
