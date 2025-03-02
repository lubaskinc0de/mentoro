from crudik.application.errors.common import ApplicationError


class SwipedMentorNotFoundError(ApplicationError): ...


class MentorAlreadySwipedError(ApplicationError): ...
