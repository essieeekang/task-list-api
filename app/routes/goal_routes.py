from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model
from .route_utilities import get_models_with_filters
from ..db import db


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)

    return {"goal": goal.to_dict()}


@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task in goal.tasks:
        task.goal_id = None

    tasks = [validate_model(Task, id) for id in request_body["task_ids"]]

    for task in tasks:
        task.goal_id = goal_id

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": request_body["task_ids"]
    }

    return response, 200


@bp.get("/<goal_id>/tasks")
def get_all_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()
    response["tasks"] = [task.to_dict() for task in goal.tasks]

    return response, 200
