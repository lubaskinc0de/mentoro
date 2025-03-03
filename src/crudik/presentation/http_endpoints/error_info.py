from crudik.adapters.file_manager import FileUploadError
from crudik.adapters.idp import UnauthorizedError
from crudik.application.errors.common import AccessDeniedError, ApplicationError
from crudik.application.errors.mentor_errors import MentorDoesNotExistsError
from crudik.application.errors.mentoring_request import (
    MentoringRequestCannotBeDeletedError,
    MentoringRequestCannotBeUpdatedError,
    MentoringRequestNotFoundError,
)
from crudik.application.errors.review_errors import ReviewDoesNotExistsError
from crudik.application.errors.student_errors import StudentDoesNotExistsError
from crudik.application.errors.swiped_mentor import SwipedMentorNotFoundError
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
    ReviewDoesNotExistsError: 404,
    MentoringRequestNotFoundError: 404,
    MentoringRequestCannotBeUpdatedError: 400,
    MentoringRequestCannotBeDeletedError: 409,
    SwipedMentorNotFoundError: 404,
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
    MentoringRequestNotFoundError: "MENTORING_REQUEST_NOT_FOUND_ERROR",
    MentoringRequestCannotBeUpdatedError: "MENTORING_REQUEST_CANNOT_BE_UPDATED_ERROR",
    MentoringRequestCannotBeDeletedError: "MENTORING_REQUEST_CANNOT_BE_DELETED_ERROR",
    SwipedMentorNotFoundError: "SWIPED_MENTOR_NOT_FOUND_ERROR",
}
