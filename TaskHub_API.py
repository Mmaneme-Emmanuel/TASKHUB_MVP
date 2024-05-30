#!/usr/bin/python3
#This is my API Resources

from flask import request, session
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from TaskHub_models import db, User, Task

# API resource class for signup
class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Signup successful'}, 201

# API resource class for signin
class SigninResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return {'message': 'Signin successful'}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

# API get resource class for user todo list
class TodoResource(Resource):
    def get(self):
        if 'user_id' not in session:
            return {'message': 'Signin required'}, 401

        user_tasks = Task.query.filter_by(user_id=session['user_id']).all()
        tasks = [{'id': task.id, 'task': task.task} for task in user_tasks]
        return {'tasks': tasks}, 200

    def post(self):
        if 'user_id' not in session:
            return {'message': 'Signin required'}, 401

        data = request.get_json()
        task_description = data.get('task')
        user_id = session['user_id']

        new_task = Task(user_id=user_id, task=task_description)
        db.session.add(new_task)
        db.session.commit()

        return {'message': 'Task added successfully'}, 201
