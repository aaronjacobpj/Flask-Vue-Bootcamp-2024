"""Connect Celery to Flask.

Every task runs inside the Flask app context, so tasks can use
db, models and render_template exactly like a normal route.
"""
from celery import Celery, Task
from celery.schedules import crontab


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name)
    celery.config_from_object(app.config["CELERY"])
    celery.Task = FlaskTask

    # ---- Scheduled jobs (run by `celery beat`) ----
    celery.conf.beat_schedule = {
        "daily-reminder": {
            "task": "application.tasks.daily_reminders",
            "schedule": crontab(hour=18, minute=0),  # every day 6 PM
            # For a quick demo replace with:  "schedule": 60.0  (every minute)
        },
        "monthly-report": {
            "task": "application.tasks.monthly_reports",
            "schedule": crontab(minute="*"),  # 1st of every month
        },
    }

    celery.set_default()
    app.extensions["celery"] = celery
    return celery
