from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    select_auth = State()
    select_entity = State()


class MentorSignUpStates(StatesGroup):
    enter_full_name = State()
    enter_about_us = State()
    enter_skills = State()
    enter_photo = State()
    sign_in = State()


class MentorSignInStates(StatesGroup):
    enter_name = State()


class MentorProfileStates(StatesGroup):
    profile = State()
    requests = State()
