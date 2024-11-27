from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.backoffice.instructor.infrastructure.controllers.flask_restx import AllInstructorsController
from modules.backoffice.instructor.infrastructure.controllers.flask_restx import InstructorFinderController
from modules.backoffice.instructor.infrastructure.controllers.flask_restx import InstructorCreatorController
from modules.backoffice.instructor.infrastructure.controllers.flask_restx import InstructorDeleterController

namespace = Namespace(name="instructor", description="Instructors")


@namespace.route("/")
class ListInstructor(Resource):
    def get(self):
        all_instructors_controller = AllInstructorsController()
        response = all_instructors_controller()
        return response

    def post(self):
        data = request.json
        instructor_creator_controller = InstructorCreatorController()
        response = instructor_creator_controller(body=data)
        return response


@namespace.route("/<string:instructor_id>")
class Instructor(Resource):
    def get(self, instructor_id):
        instructor_finder_controller = InstructorFinderController()
        response = instructor_finder_controller(instructor_id=instructor_id)
        return response

    def delete(self, instructor_id):
        instructor_deleter_controller = InstructorDeleterController()
        response = instructor_deleter_controller(instructor_id=instructor_id)
        return response
