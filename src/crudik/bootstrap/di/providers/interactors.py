from dishka import Provider, Scope, provide_all

from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent
from crudik.application.student.interactors.sign_in import SignInStudent
from crudik.application.student.interactors.sign_up import SignUpStudent
from crudik.application.student.interactors.update import UpdateStudent


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        SignUpStudent,
        SignInStudent,
        AttachAvatarToStudent,
        UpdateStudent,
    )
