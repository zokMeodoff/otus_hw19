import pytest
from django.test import Client
from django.contrib.auth.models import User
import json

client = Client()


def create_test_user(username='TestUser',
                     email='testuser@email.com',
                     first_name='Test',
                     last_name='User',
                     password='12345'):

    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    user.save()
    return user


@pytest.fixture()
def user_data_register():
    return {
        'username': 'NewTestUser',
        'password': 123456,
        'email': 'newtestuser@email.com',
        'first_name': 'Newtest',
        'last_name': 'User'
    }


@pytest.mark.django_db
def test_register_view_get():
    response_from_url = client.get('/users/')
    assert response_from_url.status_code == 405


@pytest.mark.django_db
def test_register_success(user_data_register):
    request_json = json.dumps(user_data_register)
    response_from_url = client.post('/users/', data=request_json, content_type='application/json')

    user = User.objects.first()

    assert response_from_url.status_code == 201
    assert user.username == user_data_register['username']
    assert user.email == user_data_register['email']
    assert user.first_name == user_data_register['first_name']
    assert user.last_name == user_data_register['last_name']
    assert user.is_staff is False


@pytest.mark.django_db
def test_register_fail_without_password(user_data_register):
    del user_data_register['password']
    request_json = json.dumps(user_data_register)
    response_from_url = client.post('/users/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400


@pytest.mark.django_db
def test_register_fail_without_username(user_data_register):
    del user_data_register['username']
    request_json = json.dumps(user_data_register)
    response_from_url = client.post('/users/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400


@pytest.mark.django_db
def test_login_success():
    create_test_user()
    request = {
        'username': 'TestUser',
        'password': 12345
    }

    user = User.objects.get(username='TestUser')

    request_json = json.dumps(request)
    response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 200
    assert user.is_authenticated is True


@pytest.mark.django_db
def test_login_wrong_password():
    create_test_user()
    request = {
        'username': 'TestUser',
        'password': 1234
    }

    request_json = json.dumps(request)
    response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400


@pytest.mark.django_db
def test_login_wrong_username():
    create_test_user()
    request = {
        'username': 'Test',
        'password': 12345
    }

    request_json = json.dumps(request)
    response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400


@pytest.mark.django_db
def test_login_without_password():
    create_test_user()
    request = {
        'username': 'TestUser'
    }

    request_json = json.dumps(request)
    response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400


@pytest.mark.django_db
def test_login_without_username():
    create_test_user()
    request = {
        'password': 12345
    }

    request_json = json.dumps(request)
    response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

    assert response_from_url.status_code == 400
