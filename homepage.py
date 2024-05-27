from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database

# Initialize the database with the Flask app
db.init_app(app)

@app.route ('/')
def home():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user instance
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('todo'))
    return render_template('TaskHub-signup.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Query the user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and if password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('todo'))
        else:
            return 'Invalid username or password'
    
    return render_template('TaskHub-signin.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        task_description = request.form.get('task')
        user_id = session['user_id']

        # Create a new task instance
        new_task = Task(user_id=user_id, task=task_description)
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for('todo'))

    # Fetch all tasks for the logged-in user
    user_tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('todo.html', tasks=user_tasks)

if __name__ == "__main__":
    # Create the database and the database table(s)
    with app.app_context():
        db.create_all()

    app.run(debug=True)