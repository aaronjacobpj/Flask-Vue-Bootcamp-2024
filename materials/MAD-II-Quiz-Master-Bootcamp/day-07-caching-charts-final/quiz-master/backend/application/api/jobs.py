"""APIs that start background jobs and report their status.

Async export flow (frontend):
  POST /api/export                  -> {task_id}            (job queued in Redis)
  GET  /api/export/<task_id>        -> {state: PENDING|SUCCESS|FAILURE}  (poll)
  GET  /api/export/<task_id>/file   -> the CSV file           (when SUCCESS)
"""
from celery.result import AsyncResult
from flask import Blueprint, current_app, jsonify, send_from_directory
from flask_security import auth_required, roles_required, current_user

from ..tasks import export_csv, daily_reminders, monthly_reports
from ..utils import error

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api")


@jobs_bp.post("/export")
@auth_required("token")
def start_export():
    task = export_csv.delay(current_user.id, current_user.has_role("admin"))
    return jsonify(task_id=task.id), 202


@jobs_bp.get("/export/<task_id>")
@auth_required("token")
def export_status(task_id):
    return jsonify(state=AsyncResult(task_id).state)


@jobs_bp.get("/export/<task_id>/file")
@auth_required("token")
def export_file(task_id):
    result = AsyncResult(task_id)
    if result.state != "SUCCESS":
        return error("File is not ready yet", 409)
    filename = result.result
    # a user may only download their own file; admin files only by admin
    allowed = "admin_" if current_user.has_role("admin") else f"user{current_user.id}_"
    if not filename.startswith(allowed):
        return error("Not your file", 403)
    return send_from_directory(current_app.config["EXPORT_DIR"], filename, as_attachment=True)


# --- Admin: run the scheduled jobs right now (handy for demos / viva) ---
@jobs_bp.post("/admin/jobs/<name>")
@auth_required("token")
@roles_required("admin")
def run_job(name):
    if name == "reminders":
        task = daily_reminders.delay()
    elif name == "monthly-report":
        task = monthly_reports.delay(current_month=True)
    else:
        return error("Unknown job", 404)
    return jsonify(task_id=task.id, message=f"{name} job started"), 202
