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

        hashed_password = generate_password_hash(password)
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
            # session['user_id'] = user.id
            return {
                'message': 'Signin successful',
                'data': user.toDict(),
                }, 200
        else:
            return {'message': 'Invalid username or password'}, 401

# API get resource class for user todo list
class TodoResource(Resource):
    def get(self):
        userId = request.args.get('user_id')

        if not userId:
            return {
                "status": "fail",
                "message": "Bad Request"
            }, 400

        user_tasks = Task.query.filter_by(user_id=userId).all()
        tasks = [task.toDict() for task in user_tasks]
        return {
            'status': 'Success',
            'tasks': tasks
            }, 200

    def post(self):
        data = request.get_json()

        if not data:
            return {
                "status": "fail",
                "message": "Bad Request"
            }, 400
        
        if 'user_id' not in data:
            return {'message': 'Signin required'}, 401
        
        task_description = data.get('task')
        user_id = data['user_id']

        if not task_description:
            return {'message': 'Task description cannot be empty'}, 400

        new_task = Task(user_id=user_id, task=task_description)
        db.session.add(new_task)
        db.session.commit()

        return {
            'message': 'Task added successfully',
            'data': new_task.toDict()
        }, 201


if __name__ == '__main__':
    db.create_all()
    with app.app_context():
        app.run(debug=True, host='127.0.0.1', port=5000)
