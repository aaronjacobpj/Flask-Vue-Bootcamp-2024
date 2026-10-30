"""Optional: load demo data so the UI is not empty.
Run once:  python seed_demo.py
"""
from datetime import date, timedelta

from flask_security import hash_password

from app import app
from application.extensions import db
from application.models import Subject, Chapter, Quiz, Question

DEMO = {
    "Python": {
        "Basics": [
            ("What is the output of print(2 ** 3)?", ["6", "8", "9", "5"], 2),
            ("Which keyword defines a function?", ["func", "def", "lambda", "fn"], 2),
            ("Which type is immutable?", ["list", "dict", "tuple", "set"], 3),
        ],
        "Data Structures": [
            ("len({'a': 1, 'b': 2}) is", ["1", "2", "3", "Error"], 2),
            ("Which method adds to the end of a list?", ["add", "push", "append", "insert"], 3),
        ],
    },
    "Web Development": {
        "HTTP": [
            ("Which status code means Not Found?", ["200", "301", "404", "500"], 3),
            ("Which method is idempotent?", ["POST", "PUT", "PATCH", "CONNECT"], 2),
        ],
        "Vue.js": [
            ("Which directive renders a list?", ["v-if", "v-for", "v-model", "v-bind"], 2),
            ("Vuex state is changed via", ["actions directly", "mutations", "getters", "props"], 2),
        ],
    },
}

with app.app_context():
    ds = app.extensions["security"].datastore
    if not ds.find_user(email="user@quizmaster.com"):
        ds.create_user(email="user@quizmaster.com", password=hash_password("user123"),
                       full_name="Demo User", qualification="B.Sc", roles=["user"])

    for i, (subject_name, chapters) in enumerate(DEMO.items()):
        if Subject.query.filter_by(name=subject_name).first():
            continue
        subject = Subject(name=subject_name, description=f"All about {subject_name}")
        db.session.add(subject)
        for j, (chapter_name, questions) in enumerate(chapters.items()):
            chapter = Chapter(subject=subject, name=chapter_name, description=f"{chapter_name} chapter")
            quiz = Quiz(chapter=chapter, title=f"{chapter_name} Quiz 1", time_duration=5,
                        date_of_quiz=date.today() + timedelta(days=i + j))
            for statement, options, correct in questions:
                quiz.questions.append(Question(statement=statement, option1=options[0], option2=options[1],
                                               option3=options[2], option4=options[3], correct_option=correct))
            db.session.add(chapter)
    db.session.commit()
    print("Demo data loaded. Login as user@quizmaster.com / user123")
