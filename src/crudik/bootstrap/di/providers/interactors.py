from dishka import Provider, Scope, provide_all

from crudik.application.mentor.interactors.read import ReadMentor
from crudik.application.mentor.interactors.sign_in import SignInMentor
from crudik.application.mentor.interactors.sign_up import SignUpMentor
from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent
from crudik.application.student.interactors.read_student import ReadStudent
from crudik.application.student.interactors.sign_in import SignInStudent
from crudik.application.student.interactors.sign_up import SignUpStudent
from crudik.application.student.interactors.update import UpdateStudent


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        SignUpStudent,
        SignInStudent,
        AttachAvatarToStudent,
        ReadStudent,
        SignUpMentor,
        SignInMentor,
        UpdateStudent,
        ReadMentor,
    )
