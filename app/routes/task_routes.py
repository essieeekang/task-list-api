from flask import Blueprint, request, Response
from app.models.task import Task
from .route_utilities import validate_model, create_model
from .route_utilities import get_models_with_filters
from ..db import db
from datetime import datetime
import requests
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)


@bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)

    return {"task": task.to_dict()}


@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<id>/mark_incomplete")
def marks_task_incomplete(id):
    task = validate_model(Task, id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<id>/mark_complete")
def marks_task_complete(id):
    task = validate_model(Task, id)
    task.completed_at = datetime.now()
    db.session.commit()

    data = {
        "token": os.environ.get('SLACKBOT_TOKEN'),
        "channel": "all-ada-testing",
        "text": f"Someone just complete the task {task.title}"
    }

    requests.post(
        "https://slack.com/api/chat.postMessage",
        data=data)

    return Response(status=204, mimetype="application/json")
