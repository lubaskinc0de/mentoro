from crudik.application.common.errors import ApplicationError


class MentoringRequestNotFoundError(ApplicationError):
    pass


class MentoringRequestCannotBeUpdatedError(ApplicationError):
    pass
