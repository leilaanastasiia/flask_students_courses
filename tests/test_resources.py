import json
from setup import GROUP_LIST, FIRST_NAMES_LIST, LAST_NAMES_LIST, COURSES_DICT

########################################################################
'''TEST INDEX'''
########################################################################

def test_index(client, index_data):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the '/' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('/')
    decoded_data = json.loads(response.data)
    assert decoded_data == index_data
    assert response.status_code == 200

########################################################################
'''TEST GROUPS'''
########################################################################

def test_groups_all(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/groups/' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/groups/')
    decoded_data = json.loads(response.data)
    for item in decoded_data:
        assert item['name'] in GROUP_LIST
    assert decoded_data[0]['number_of_students'] in range(0, 40)
    assert len(decoded_data) == 10
    assert response.status_code == 200


def test_courses_count(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/groups/?students_count=20' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/groups/?students_count=20')
    decoded_data = json.loads(response.data)
    for item in decoded_data:
        assert item['number_of_students'] in range(21)
    assert response.status_code == 200


def test_courses_count_smaller(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/groups/?students_count=3' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/groups/?students_count=3')
    decoded_data = json.loads(response.data)
    assert decoded_data == {'response': "Enter a bigger student's count number"}
    assert response.status_code == 200

########################################################################
'''TEST STUDENTS'''
########################################################################

def test_students_all(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/students/' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/students/')
    decoded_data = json.loads(response.data)
    for item in decoded_data:
        name = item['student_name'].split(' ')
        assert name[0] in FIRST_NAMES_LIST
        assert name[1] in LAST_NAMES_LIST
        assert item['students_id'] in range(201)
        assert item['course_name'] in COURSES_DICT.keys()
    assert response.status_code == 200


def test_students_biology(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/students/?course_name=Biology' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/students/?course_name=Biology')
    decoded_data = json.loads(response.data)
    for item in decoded_data:
        assert item['course_name'] == 'Biology'
    assert response.status_code == 200


def test_students_course_not_exist(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/students/?course_name=Magic' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/students/?course_name=Magic')
    decoded_data = json.loads(response.data)
    assert decoded_data == {
                        'response': "No such course has been found. ",
                        'available courses': 'Mathematics, Biology, Economics, Philosophy, '
                                            'Engineering, Tactical medicine, Politics, '
                                            'Psychology, Art or Methodology'}
    assert response.status_code == 200


def test_new_students(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/students/' page is requested (POST)
        THEN check that the response is valid
        """
    parameters = {'first_name': 'test_first_name', 'last_name': 'test_last_name', 'group_id': 5}
    response = client.post('http://127.0.0.1:5000/api/v1/students/',
                           headers={"Content-Type": "application/json"},
                           data=json.dumps(parameters))
    decoded_data = json.loads(response.data)
    assert decoded_data == {
                'response': f"Student {parameters['first_name']} "
                            f"{parameters['last_name']} was successfully added"
            }
    assert response.status_code == 201

def test_delete_students(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/students/' page is requested (DELETE)
        THEN check that the response is valid
        """
    parameters = {'id': '209'}  # id must exists
    response = client.delete('http://127.0.0.1:5000/api/v1/students/',
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(parameters))
    decoded_data = json.loads(response.data)
    assert decoded_data == {
                'response': f"Student with an id {parameters['id']} was successfully deleted"
            }
    assert response.status_code == 200

########################################################################
'''TEST COURSES'''
########################################################################

def test_courses_all(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/courses/' page is requested (GET)
        THEN check that the response is valid
        """
    response = client.get('http://127.0.0.1:5000/api/v1/courses/')
    decoded_data = json.loads(response.data)
    for item in decoded_data:
        assert item['course_id'] in range(11)
        assert item['course_name'] in COURSES_DICT.keys()
        assert item['course_description'] in COURSES_DICT.values()
        assert isinstance(item['students'], list)
    assert response.status_code == 200


def test_new_students_course(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/courses/' page is requested (POST)
        THEN check that the response is valid
        """
    parameters = {'course_id': 1, 'student_id': 1}
    response = client.post('http://127.0.0.1:5000/api/v1/courses/',
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(parameters))
    decoded_data = json.loads(response.data)
    assert decoded_data == {
        'response': f"Student with an id of {parameters['student_id']} was added to the chosen course"
    }
    assert response.status_code == 201


def test_delete_students_course(client):
    """
        GIVEN a Flask application configured for testing in config.py
        WHEN the 'http://127.0.0.1:5000/api/v1/courses/' page is requested (DELETE)
        THEN check that the response is valid
        """
    parameters = {'course_id': 1, 'student_id': 1}  # id must exists
    response = client.delete('http://127.0.0.1:5000/api/v1/courses/',
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(parameters))
    decoded_data = json.loads(response.data)
    assert decoded_data == {
                'response': f"Student with an id of {parameters['student_id']} was deleted "
                            f"from the course with an id of {parameters['course_id']}"
            }
    assert response.status_code == 200