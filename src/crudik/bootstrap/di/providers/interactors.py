from dishka import Provider, Scope, provide_all

from crudik.application.student.interactors.sign_up import SignUpStudent


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        SignUpStudent,
    )
