from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    correct_answer = db.Column(db.String(50), nullable=False)

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)

# Function to initialize the database with questions
def initialize_database():
    with app.app_context():
        db.create_all()
        if not QuizQuestion.query.first():
            questions = [
                QuizQuestion(question_text="What is your favorite color?", option1="Red", option2="Blue", option3="Green", correct_answer="Blue"),
                QuizQuestion(question_text="What is your favorite animal?", option1="Dog", option2="Cat", option3="Parrot", correct_answer="Dog")
            ]
            db.session.bulk_save_objects(questions)
            db.session.commit()

@app.route('/')
def index():
    return render_template('quiz.html')

@app.route('/get_questions', methods=['GET'])
def get_questions():
    questions = QuizQuestion.query.all()
    questions_data = [
        {"id": q.id, "text": q.question_text, "options": [q.option1, q.option2, q.option3]}
        for q in questions
    ]
    return jsonify({"questions": questions_data})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    username = data['username']
    answers = data['answers']

    # Calculate the score
    score = 0
    total_questions = len(answers)
    for qid, answer in answers.items():
        question = QuizQuestion.query.get(int(qid))
        if question and question.correct_answer == answer:
            score += 1

    # Calculate percentage score
    score_percent = (score / total_questions) * 100 if total_questions > 0 else 0

    # Save the score in the database
    user_score = UserScore(username=username, score=score_percent)
    db.session.add(user_score)
    db.session.commit()

    # Get best score
    best_score = db.session.query(db.func.max(UserScore.score)).scalar()

    return jsonify({
        "username": username,
        "score": score_percent,
        "best_score": best_score
    })

if __name__ == '__main__':
    # Initialize the database with sample data
    initialize_database()
    # Run the Flask app
    app.run(debug=True)
