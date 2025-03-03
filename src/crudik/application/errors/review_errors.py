from crudik.application.errors.common import ApplicationError


class ReviewDoesNotExistsError(ApplicationError): ...


class ReviewCannotBeAddedError(ApplicationError): ...
