#!/usr/bin/python3
from flask import Flask
from flask_restful import Api
from TaskHub_models import db

# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize the database with the Flask app
db.init_app(app)

# Create the API object
api = Api(app)

# Import and add the API resources
from TaskHub_API import SignupResource, SigninResource, TodoResource

api.add_resource(SignupResource, '/api/signup')
api.add_resource(SigninResource, '/api/signin')
api.add_resource(TodoResource, '/api/todo')

if __name__ == "__main__":
    # Create the database and the database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)
