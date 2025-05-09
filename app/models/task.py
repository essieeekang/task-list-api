from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at if self.completed_at else False
        }

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            new_task = cls(
                title=task_data["title"],
                description=task_data["description"],
                completed_at=task_data["completed_at"])
        else:
            new_task = cls(
                title=task_data["title"],
                description=task_data["description"])

        return new_task
