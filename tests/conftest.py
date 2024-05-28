import pytest

from courses_app import app as my_app


@pytest.fixture()
def app():
    app = my_app
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def index_data():
    data = {
                'Groups': 'http://127.0.0.1:5000/api/v1/groups/?students_count=20',
                'Students': 'http://127.0.0.1:5000/api/v1/students/?course_name=Biology',
                'Courses' : 'http://127.0.0.1:5000/api/v1/courses/'
            }
    return data


