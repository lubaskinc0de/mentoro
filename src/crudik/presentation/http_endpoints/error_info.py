from crudik.adapters.file_manager import FileUploadError
from crudik.adapters.idp import UnauthorizedError
from crudik.application.common.errors import AccessDeniedError, ApplicationError
from crudik.application.mentor.errors import MentorDoesNotExistsError
from crudik.application.review.errors import ReviewDoesNotExistsError
from crudik.application.student.errors import StudentDoesNotExistsError
from crudik.presentation.http_endpoints.student import (
    CannotReadFileInfoError,
    CannotReadFileSizeError,
    FileIsNotImageError,
    FileTooBigError,
)

error_code = {
    ApplicationError: 500,
    StudentDoesNotExistsError: 404,
    MentorDoesNotExistsError: 404,
    FileUploadError: 422,
    UnauthorizedError: 401,
    FileIsNotImageError: 422,
    FileTooBigError: 413,
    CannotReadFileSizeError: 400,
    CannotReadFileInfoError: 400,
    AccessDeniedError: 403,
}
error_unique_code = {
    ApplicationError: "APPLICATION_ERROR",
    StudentDoesNotExistsError: "STUDENT_DOES_NOT_EXISTS_ERROR",
    MentorDoesNotExistsError: "MENTOR_DOES_NOT_EXISTS_ERROR",
    FileUploadError: "FILE_UPLOAD_ERROR",
    UnauthorizedError: "UNAUTHORIZED_ERROR",
    FileIsNotImageError: "FILE_IS_NOT_IMAGE_ERROR",
    FileTooBigError: "FILE_TOO_BIG_ERROR",
    CannotReadFileSizeError: "CANNOT_READ_FILE_SIZE_ERROR",
    CannotReadFileInfoError: "CANNOT_READ_FILE_INFO_ERROR",
    ReviewDoesNotExistsError: "REVIEW_DOES_NOT_EXISTS_ERROR",
    AccessDeniedError: "ACCESS_DENIED_ERROR",
}
