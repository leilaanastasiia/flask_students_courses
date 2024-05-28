from flask import make_response, request, jsonify
from flask_restful import Resource
from sqlalchemy import select, insert, delete

from courses_app.models import get_session, Course, association_table


class Courses(Resource):
    headers = {'content-type': 'application/json'}

    def get(self):
        """Show all courses info with its students"""
        headers = self.headers
        with get_session() as session:
            statement = (
                select(Course)
                .order_by(Course.id))
            data = session.execute(statement).all()
            resp = []
            for item in data:
                resp.append({
                    'course_id': item.Course.id,
                    'course_name': item.Course.name,
                    'course_description': item.Course.description,
                    'students': [f"{student.id}: {student.first_name} {student.last_name}"
                                for student in item.Course.students]
                })
            return make_response(jsonify(resp), 200, headers)

    def post(self):
        """Add a new student to the course """
        json_data = request.get_json()
        course_id_param = json_data['course_id']
        student_id_param = json_data['student_id']
        headers = self.headers
        with get_session() as session:
            statement =(
                insert(association_table)
                .returning(association_table))
            params = [{'student_id': student_id_param, 'course_id': course_id_param}]
            data = session.scalars(statement, params).all()
            session.commit()
            resp = {
                'response': f"Student with an id of {data[0]} was added to the chosen course"
            }
            return make_response(jsonify(resp), 201, headers)

    def delete(self):
        """Remove the student from one of his or her courses """
        json_data = request.get_json()
        course_id_param = json_data['course_id']
        student_id_param = json_data['student_id']
        headers = self.headers
        with get_session() as session:
            statement =(
                delete(association_table)
                .where(association_table.columns.student_id == student_id_param)
                .where(association_table.columns.course_id == course_id_param)
                .returning(association_table))
            data = session.execute(statement).all()
            session.commit()
            resp = {
                'response': f"Student with an id of {data[0][0]} was deleted "
                            f"from the course with an id of {data[0][1]}"
            }
            return make_response(jsonify(resp), 200, headers)