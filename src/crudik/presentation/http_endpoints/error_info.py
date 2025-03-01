from crudik.application.common.errors import ApplicationError
from crudik.application.student.errors import StudentDoesNotExistsError

error_code = {
    ApplicationError: 500,
    StudentDoesNotExistsError: 404,
}
error_unique_code = {
    ApplicationError: "APPLICATION_ERROR",
    StudentDoesNotExistsError: "STUDENT_DOES_NOT_EXISTS_ERROR",
}
