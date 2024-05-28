from flask import make_response, request, jsonify
from flask_restful import Resource
from sqlalchemy import select, insert, delete

from courses_app.models import get_session, Student, Course


class Students(Resource):
    headers = {'content-type': 'application/json'}

    def get(self):
        """Find all students related to the course with a given name"""
        course_name_param = request.args.get('course_name')
        headers = self.headers
        with get_session() as session:
            subquery = (
                select(Student.id, Student.first_name, Student.last_name, Course.name)
                .join(Student.courses)
                .order_by(Student.id))
            data = session.execute(subquery).all()
            if course_name_param:
                course_names = [course.name for course in data]
                if course_name_param in course_names:
                    data = session.execute(subquery
                                        .where(Course.name == course_name_param)
                                        ).all()
                if course_name_param not in course_names:
                    resp = {
                        'response': "No such course has been found. ",
                        'available courses': 'Mathematics, Biology, Economics, Philosophy, '
                                            'Engineering, Tactical medicine, Politics, '
                                            'Psychology, Art or Methodology'}
                    return make_response(jsonify(resp), 200, headers)
            resp = []
            for item in data:
                resp.append({
                    'students_id': item.id,
                    'student_name': item.first_name + ' ' + item.last_name,
                    'course_name': item.name
                })
            return make_response(jsonify(resp), 200, headers)

    def post(self):
        """Add a new student """
        json_data = request.get_json()
        first_name_param = json_data['first_name']
        last_name_param = json_data['last_name']
        group_id_param = json_data['group_id']
        headers = self.headers
        with get_session() as session:
            statement= (
                insert(Student)
                .returning(Student))
            params = [{
                'first_name': first_name_param,
                'last_name': last_name_param,
                'group_id': group_id_param
            }]
            data = session.scalars(statement, params).all()
            session.commit()
            resp = {
                'response': f"Student {data[0].first_name} {data[0].last_name} was successfully added"
            }
            return make_response(jsonify(resp), 201, headers)

    def delete(self):
        """Delete a student by STUDENT_ID """
        json_data = request.get_json()
        id_param = json_data['id']
        headers = self.headers
        with get_session() as session:
            statement = (
                delete(Student)
                .where(Student.id == id_param)
                .returning(Student.id)
            )
            data = session.scalars(statement).all()
            session.commit()
            resp = {
                'response': f"Student with an id {data[0]} was successfully deleted"
            }

            return make_response(jsonify(resp), 200, headers)