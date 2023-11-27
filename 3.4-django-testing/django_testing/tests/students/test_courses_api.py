import json
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student



@pytest.fixture
def client():
    return APIClient()


# создает пользователя и возвращает его
@pytest.fixture
def user():
    return Student.objects.create(name='Sblushin')


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory





def test_example():
    assert True, "Just test example"


@pytest.mark.django_db
def test_get_courses(client, user):
    # Arrange
    course = Course.objects.create(name='Mathematics')
    course.students.add(user)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Mathematics'



@pytest.mark.django_db
def test_create_course(client, user, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name

