from flask_sqlalchemy import SQLAlchemy
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


def load_questions():
    file_path = os.path.join("data", "questions.json")
    abs_file_path = os.path.abspath(file_path)
    print("Absolute path to questions.json:", abs_file_path)

    with open(file_path, "r") as file:
        questions = json.load(file)
    return questions


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    game_count = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    scores = db.relationship('Score', backref='user', lazy=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])  # Fixed the route decorator
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already in use')
            return redirect(url_for('register'))

        new_user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    users = User.query.order_by(User.score.desc()).all()
    return render_template('dashboard.html', username=current_user.username, users=users)

@app.route('/game/', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'POST':
        # Implement game logic here
        questions = load_questions()
        correct_answers = 0

        for i, question in enumerate(questions):
            user_answer = request.form.get(f'question_{i + 1}')
            if user_answer == question['correct_answer']:
                correct_answers += 1

        # Update user score and games played count
        current_user.score += correct_answers * 10
        current_user.games_played += 1
        db.session.commit()

        percentage = (correct_answers / len(questions)) * 100
        return render_template('results.html', correct_answers=correct_answers, percentage=percentage)

    # Load trivia questions from JSON file and render game template
    all_questions = load_questions()
    questions = random.sample(all_questions, 15)  # Select 15 random questions
    return render_template('game.html', questions=questions)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/game/quit')
@login_required
def quit_game():
    # Load trivia questions from JSON file
    all_questions = load_questions()
    questions = random.sample(all_questions, 15)  # Select 15 random questions

    # Get the number of unanswered questions
    unanswered_questions = len(questions) - int(request.args.get("answered_questions", 0))

    # Calculate the penalty for quitting the game early
    penalty = 25 * unanswered_questions

    # Update the user's score and games played count
    current_user.score -= penalty
    current_user.games_played += 1
    db.session.commit()

    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)

