from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('Add your name')
        password = request.form.get('Add your password')
        email = request.form.get('add a valid email')
        
        # Handle the sign-up logic (e.g., save to database)
        print(f"Username: {username}, Password: {password}, Email: {email}")

        # Assuming you have a User model defined for database operations

    return render_template('signup.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('Add your name')
        password = request.form.get('Add your password')

        # This section checks if user exists and password matches
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    
    return render_template('signin.html')

if __name__ == "__main__":
    app.run(debug=True)


       