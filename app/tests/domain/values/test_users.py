from datetime import datetime
from faker import Faker
import pytest

from domain.entities.users import User
from domain.exceptions.users import UsernameTooLongException, EmptyUsernameException, EmptyPasswordException, \
    PasswordTooLongException, PasswordTooSmallException, EmailTooSmallException, EmailTooLongException, \
    EmptyEmailException, InvalidEmailException
from domain.values.users import Username, Password, Email


def test_create_user_success(
        faker: Faker
):
    username = Username('Petya')
    email = Email('Petya489@gmail.com')
    password = Password('petrovi448')

    user = User(
        username=username,
        email=email,
        password=password
    )

    assert user.username == username
    assert user.email == email
    assert user.password == password  # TODO Add password hasher to entity and tests
    assert user.created_at.date() == datetime.today().date()


def test_create_user_username_too_long(faker: Faker):
    with pytest.raises(UsernameTooLongException):
        username = faker.text(max_nb_chars=333)
        Username(username)


def test_create_user_empty_username():
    with pytest.raises(EmptyUsernameException):
        username = Username('')


def test_create_user_empty_password():
    with pytest.raises(EmptyPasswordException):
        Password('')


def test_create_user_email_too_long(faker: Faker):
    with pytest.raises(EmailTooLongException):
        email = faker.email() * 10
        email = Email(email)
        raise EmailTooLongException(email)


def test_create_user_email_too_short():
    with pytest.raises(EmailTooSmallException):
        email = Email('aa@a')
        raise EmailTooSmallException(email)


def test_create_user_invalid_email(faker: Faker):
    with pytest.raises(InvalidEmailException):
        email = faker.email().replace('@', '')
        Email(email)


def test_create_user_empty_email():
    with pytest.raises(EmptyEmailException):
        Email('')


