from crudik.application.common.errors import ApplicationError


class SwipedMentorNotFoundError(ApplicationError): ...


class MentorAlreadySwipedError(ApplicationError): ...
