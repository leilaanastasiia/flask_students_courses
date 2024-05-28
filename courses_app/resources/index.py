from flask import make_response
from flask_restful import Resource


class Index(Resource):
    headers = {'content-type': 'application/json'}

    """ Exist only for quick navigation from a browser"""
    def get(self):
            resp = {
                'Groups': 'http://127.0.0.1:5000/api/v1/groups/?students_count=20',
                'Students': 'http://127.0.0.1:5000/api/v1/students/?course_name=Biology',
                'Courses' : 'http://127.0.0.1:5000/api/v1/courses/'
            }
            return make_response(resp, 200, self.headers)
