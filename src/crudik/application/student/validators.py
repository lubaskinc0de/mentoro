from crudik.application.student.errors import IncorrectLengthStudentLoginError


def validate_student_login(login: str) -> None:
    if len(login) not in range(6, 100):
        raise IncorrectLengthStudentLoginError


def validate_student_password(password: str) -> None:
    pass


def validate_student_full_name(full_name: str) -> None:
    pass
