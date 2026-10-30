"""Convert model objects to plain dicts for JSON responses."""


def subject_to_dict(s, with_chapters=False):
    d = {"id": s.id, "name": s.name, "description": s.description,
         "chapter_count": len(s.chapters)}
    if with_chapters:
        d["chapters"] = [chapter_to_dict(c) for c in s.chapters]
    return d


def chapter_to_dict(c):
    return {"id": c.id, "subject_id": c.subject_id, "subject_name": c.subject.name,
            "name": c.name, "description": c.description,
            "quiz_count": len(c.quizzes)}


def quiz_to_dict(q):
    return {"id": q.id, "chapter_id": q.chapter_id, "chapter_name": q.chapter.name,
            "subject_name": q.chapter.subject.name, "title": q.title,
            "date_of_quiz": q.date_of_quiz.isoformat() if q.date_of_quiz else None,
            "time_duration": q.time_duration, "remarks": q.remarks,
            "question_count": len(q.questions)}


def question_to_dict(q, with_answer=True):
    d = {"id": q.id, "quiz_id": q.quiz_id, "statement": q.statement,
         "options": [o for o in (q.option1, q.option2, q.option3, q.option4)]}
    if with_answer:  # never send answers to a quiz taker
        d["correct_option"] = q.correct_option
    return d


def score_to_dict(s):
    return {"id": s.id, "quiz_id": s.quiz_id, "quiz_title": s.quiz.title,
            "subject_name": s.quiz.chapter.subject.name,
            "chapter_name": s.quiz.chapter.name,
            "user_id": s.user_id, "user_name": s.user.full_name,
            "attempted_at": s.time_stamp_of_attempt.isoformat(timespec="minutes"),
            "total_scored": s.total_scored, "total_questions": s.total_questions,
            "percentage": round(100 * s.total_scored / s.total_questions, 1) if s.total_questions else 0}
