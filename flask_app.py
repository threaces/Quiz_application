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
                QuizQuestion(question_text="Co oznacza skrót AI?", option1="Automated Integration", option2="Artificial Intelligence", 
                             option3="Advanced Innovation", correct_answer="Artificial Intelligence"),
                QuizQuestion(question_text="Gdzie można wykorzystać sztuczną inteligencję?", option1="Komputery", option2="Nauka", 
                             option3="Gotowanie", correct_answer="Nauka"),
                QuizQuestion(question_text="Jak nazywa się język, który wykorzystujemy, w 'rozmowie z komputerem'?", option1= "Python", 
                             option2= "Angielski", option3 = 'Język migowy', correct_answer="Python"),
                QuizQuestion(question_text="W jakich grach wykorzystamy AI?", option1="Gra w chowanego", option2= "W szachach i grach wideo", 
                             option3="Kółko i krzyżyk", correct_answer="W szachach i grach wideo"),
                QuizQuestion(question_text="Co komputer może zrobić z tekstem?", option1="Zrozumieć, przetłumaczyć lub dokończyć zadanie", 
                             option2="Sprawdzić poprawną pisownie", option3="Obie odpowiedzi są poprawne", correct_answer="Obie odpowiedzi są poprawne")
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
