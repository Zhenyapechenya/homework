import json
import pytest
from django.core.exceptions import ValidationError
from django.conf import settings
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student

# @pytest.fixture
# def client():
#     return APIClient()


# @pytest.fixture
# def message_factory():
#     def factory(*args, **kwargs):
#         return baker.make(Course, *args, **kwargs)

#     return factory



@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory



# проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    course = course_factory(_quantity=1)[0]
    
    response = client.get(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_many_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    course_id = course_factory(_quantity=100)[69].id

    response = client.get('/api/v1/courses/', {'id': f'{course_id}'})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    course_name = course_factory(_quantity=100)[69].name

    response = client.get('/api/v1/courses/', {'name': f'{course_name}'})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == course_name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    course_data = {
        'name': 'Literature'
    }

    response = client.post('/api/v1/courses/', data=course_data)

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Literature'


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_data = {
        'name': 'Musics'
    }

    response = client.patch(f'/api/v1/courses/{course[0].id}/', data=course_data)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Musics'


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    
    assert response.status_code == 204


# добавление нескольких студентов на курс
@pytest.mark.django_db
def test_get_courses(client, student_factory, course_factory):
    # Arrange
    course = course_factory(_quantity=1)[0]
    students = student_factory(_quantity=10)
    course.students.add(*students)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course.name
    assert data[0]['students'] == [s.id for s in students]
    


# проверка валидации на максимальное число студентов на курсе
@pytest.fixture
def settings_with_max_students(settings):
    settings.MAX_STUDENTS_PER_COURSE = 20
    return settings


@pytest.mark.django_db
@pytest.mark.parametrize("enrolled_students_count, should_raise_error", [
    (settings.MAX_STUDENTS_PER_COURSE - 1, False),
    (settings.MAX_STUDENTS_PER_COURSE + 1, True),
])
def test_enrollment_validation(settings_with_max_students, enrolled_students_count, should_raise_error, course_factory, student_factory):
    course = course_factory(_quantity=1)[0]
    students = student_factory(_quantity=enrolled_students_count)
    course.students.add(*students)

    if should_raise_error:
        with pytest.raises(ValidationError, match=f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}"):
            course.clean()
    else:
        course.clean()
