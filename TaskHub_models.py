#!/usr/bin/python3
#This file is my Database Models

from flask_sqlalchemy import SQLAlchemy
# Create SQLAlchemy database instance
db = SQLAlchemy()

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    
    tasks = db.relationship('Task', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.username}>"

# Define Task model
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return f"<Task {self.task} by User {self.user_id}>"
