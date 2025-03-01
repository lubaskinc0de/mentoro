from dishka import Provider, Scope, provide_all

from crudik.application.mentor.interactors.sign_in import SignInMentor
from crudik.application.mentor.interactors.sign_up import SignUpMentor
from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent
from crudik.application.student.interactors.read_student import ReadStudent
from crudik.application.student.interactors.sign_in import SignInStudent
from crudik.application.student.interactors.sign_up import SignUpStudent


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

<<<<<<< src/crudik/bootstrap/di/providers/interactors.py
    provides = provide_all(SignUpStudent, SignInStudent, AttachAvatarToStudent, ReadStudent)
=======
    provides = provide_all(SignUpStudent, SignInStudent, AttachAvatarToStudent, ReadStudent, SignUpMentor, SignInMentor)
>>>>>>> src/crudik/bootstrap/di/providers/interactors.py
