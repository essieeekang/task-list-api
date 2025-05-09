from flask import abort, make_response
from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    sort = ""

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
            if attribute == "sort":
                sort = value

    if sort == "asc":
        models = db.session.scalars(query.order_by(cls.title.asc()))
    elif sort == "desc":
        models = db.session.scalars(query.order_by(cls.title.desc()))
    else:
        models = db.session.scalars(query.order_by(cls.id))

    models_response = [model.to_dict() for model in models]
    return models_response
