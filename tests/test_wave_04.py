# There are no tests for wave 4.
from app.routes.task_routes import send_slack_notif
from app.models.task import Task


# ------ Added Tests -------
def test_slack_notif_successful(client, one_task):
    # Arrange and Act
    response = client.patch("/tasks/1/mark_complete")

    assert response.status_code == 204


def test_send_slack_notif_helper_success(client):
    task = Task(title="Task", description="Task description")
    response = send_slack_notif(task)

    assert response.status_code == 200
    assert response.ok
