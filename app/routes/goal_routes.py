from flask import Blueprint, request, Response
from app.models.goal import Goal
from .route_utilities import validate_model, create_model
from .route_utilities import get_models_with_filters
from ..db import db


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Goal, request.args)


@bp.get("/<id>")
def get_one_task(id):
    goal = validate_model(Goal, id)

    return {"goal": goal.to_dict()}


@bp.put("/<id>")
def update_task(id):
    task = validate_model(Goal, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Goal, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
