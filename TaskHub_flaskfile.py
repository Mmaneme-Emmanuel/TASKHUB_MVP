from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from TaskHub_models import db, User, Task
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
# Set a secret key for session management
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')

# Initialize the database with the Flask app
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.')
        return redirect(url_for('signin'))
    return render_template('TaskHub-signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        # Check if user exists and if password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Signed in successfully!')
            return redirect(url_for('todo'))
        else:
            flash('Invalid username or password')
    
    return render_template('TaskHub-signin.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        flash('Please sign in to access your to-do list.')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        task_description = request.form.get('task')
        user_id = session['user_id']

        if not task_description:
            flash('Task description cannot be empty')
            return redirect(url_for('todo'))

        new_task = Task(user_id=user_id, task=task_description)
        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully')
        return redirect(url_for('todo'))

 # Fetch all tasks for the logged-in user
    user_tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('todo.html', tasks=user_tasks)

if __name__ == "__main__":
# Create the database and the database table(s)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
