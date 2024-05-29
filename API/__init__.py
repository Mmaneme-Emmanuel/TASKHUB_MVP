#This file is my API Blueprint Initialization

from flask import Blueprint
from flask_restful import Api
from TaskHub_API import SignupResource, SigninResource, TodoResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(SignupResource, '/signup')
api.add_resource(SigninResource, '/signin')
api.add_resource(TodoResource, '/todo')