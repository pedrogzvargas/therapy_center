from flask_restx import reqparse


class ParseArgs:

    @staticmethod
    def build():
        search_parser = reqparse.RequestParser()
        search_parser.add_argument("name", type=str, required=False, help="Search user by name")
        search_parser.add_argument("last_name", type=str, required=False, help="Search user by last name")
        search_parser.add_argument("page_size", type=str, required=False, default=10, help="Page size")
        search_parser.add_argument("page", type=str, required=False, default=1, help="Page number")

        return search_parser
