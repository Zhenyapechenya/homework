import json
import pytest
from rest_framework.test import APIClient

from students.models import Course, Student



@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return Student.objects.create(name='Sblushin')


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
def test_creste_course(client, user):
    response = client.post('/api/v1/courses/', data={'student': user.id, 'name': 'Physics'}, format='json')
    response.status_code == 201