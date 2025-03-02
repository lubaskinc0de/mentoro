from dishka import Provider, Scope, provide_all

from crudik.application.mentor.interactors.attach_avatar import AttachAvatarToMentor
from crudik.application.mentor.interactors.read import ReadMentor
from crudik.application.mentor.interactors.read_by_id import ReadMentorById
from crudik.application.mentor.interactors.sign_in import SignInMentor
from crudik.application.mentor.interactors.sign_up import SignUpMentor
from crudik.application.mentor.interactors.update import UpdateMentor
from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent
from crudik.application.student.interactors.find_mentor import FindMentor
from crudik.application.student.interactors.read_student import ReadStudent
from crudik.application.student.interactors.read_student_by_id import ReadStudentById
from crudik.application.student.interactors.sign_in import SignInStudent
from crudik.application.student.interactors.sign_up import SignUpStudent
from crudik.application.student.interactors.swipe_mentor import SwipeMentor
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
        UpdateMentor,
        ReadMentor,
        FindMentor,
        AttachAvatarToMentor,
        SwipeMentor,
        ReadMentorById,
        ReadStudentById,
    )
