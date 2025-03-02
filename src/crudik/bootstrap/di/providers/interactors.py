from dishka import Provider, Scope, provide_all

from crudik.application.mentor.attach_avatar import AttachAvatarToMentor
from crudik.application.mentor.read import ReadMentor
from crudik.application.mentor.read_by_id import ReadMentorById
from crudik.application.mentor.sign_in import SignInMentor
from crudik.application.mentor.sign_up import SignUpMentor
from crudik.application.mentor.update import UpdateMentor
from crudik.application.mentoring_request.delete import DeleteMentoringRequestById
from crudik.application.mentoring_request.read_all_mentor import ReadMentorMentoringRequests
from crudik.application.mentoring_request.read_all_student import ReadStudentMentoringRequests
from crudik.application.mentoring_request.send import SendMentoringByStudent
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestByMentor
from crudik.application.review.add_review import AddReview
from crudik.application.review.delete_review import DeleteReview
from crudik.application.review.read_reviews import ReadMentorReviews
from crudik.application.student.attach_avatar import AttachAvatarToStudent
from crudik.application.student.delete_favorites_mentor import DeleteFavoritesMentor
from crudik.application.student.find_mentor import FindMentor
from crudik.application.student.read_favorites_mentors import ReadFavoritesMentors
from crudik.application.student.read_student import ReadStudent
from crudik.application.student.read_student_by_id import ReadStudentById
from crudik.application.student.sign_in import SignInStudent
from crudik.application.student.sign_up import SignUpStudent
from crudik.application.student.swipe_mentor import SwipeMentor
from crudik.application.student.update import UpdateStudent


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
        ReadFavoritesMentors,
        DeleteFavoritesMentor,
        SendMentoringByStudent,
        ReadStudentMentoringRequests,
        AddReview,
        DeleteReview,
        ReadMentorReviews,
        VerdictMentoringRequestByMentor,
        ReadMentorMentoringRequests,
        DeleteMentoringRequestById,
    )
