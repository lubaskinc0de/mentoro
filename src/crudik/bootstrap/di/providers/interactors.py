from dishka import Provider, Scope, provide_all

from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent
from crudik.application.student.interactors.read_student import ReadStudent
from crudik.application.student.interactors.sign_in import SignInStudent
from crudik.application.student.interactors.sign_up import SignUpStudent


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(SignUpStudent, SignInStudent, AttachAvatarToStudent, ReadStudent)
