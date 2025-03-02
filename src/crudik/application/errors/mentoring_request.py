from crudik.application.errors.common import ApplicationError


class MentoringRequestNotFoundError(ApplicationError):
    pass


class MentoringRequestCannotBeUpdatedError(ApplicationError):
    pass
