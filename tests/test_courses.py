import pytest
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIRequestFactory
from courses.models import Course
from courses.serializers import CourseSerializer
from django.utils.timezone import now
import json

client = Client()
request_factory = APIRequestFactory()


def create_test_course(title='TestCourse'):
    course = Course.objects.create(
        title=title,
        price=100,
        date_start=now(),
        duration=5
    )
    return course


@pytest.mark.django_db
def test_one_course_view():
    create_test_course(title='TestCourse1')
    create_test_course(title='TestCourse2')
    user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
    token = Token.objects.create(user=user)

    response_from_url = client.get('/courses/1/', HTTP_AUTHORIZATION='Token {}'.format(token)).content
    request = request_factory.get('/courses/1/')
    serializer_context = {
        'request': Request(request),
    }
    course = Course.objects.get(id=1)
    serializer = CourseSerializer(course, context=serializer_context)
    test_data = JSONRenderer().render(serializer.data)
    assert test_data == response_from_url


@pytest.mark.django_db
def test_course_list_view():
    create_test_course(title='TestCourse1')
    create_test_course(title='TestCourse2')
    user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
    token = Token.objects.create(user=user)

    response_from_url = client.get('/courses/', HTTP_AUTHORIZATION='Token {}'.format(token)).content
    request = request_factory.get('/courses/')
    serializer_context = {
        'request': Request(request),
    }
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, context=serializer_context, many=True)
    test_data = JSONRenderer().render(serializer.data)
    assert test_data == response_from_url


@pytest.mark.django_db
def test_course_signup_success():
    course = create_test_course()
    user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
    token = Token.objects.create(user=user)

    client.force_login(user=user)
    request_uri = '/courses/signup/{}/'.format(course.id)
    response_from_url = client.patch(request_uri, HTTP_AUTHORIZATION='Token {}'.format(token))
    response_json = json.loads(response_from_url.content.decode('utf-8'))
    assert response_json['title'] == course.title
    assert response_from_url.status_code == 200


@pytest.mark.django_db
def test_course_signup_fail_no_such_course():
    course = create_test_course()
    user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
    token = Token.objects.create(user=user)

    client.force_login(user=user)
    request_uri = '/courses/signup/15/'
    response_from_url = client.post(request_uri, HTTP_AUTHORIZATION='Token {}'.format(token))
    assert response_from_url.status_code == 404


@pytest.mark.django_db
def test_course_signup_fail_unauthorized_user():
    course = create_test_course()

    request_uri = '/courses/signup/{}/'.format(course.id)
    response_from_url = client.post(request_uri)
    assert response_from_url.status_code == 401

