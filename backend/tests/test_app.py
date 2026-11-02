
import pytest
import backend.app as app_module


@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_get_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json == []


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Learn Docker",
            "priority": "High",
            "status": "Pending"
        }
    )

    assert response.status_code == 201
    assert response.json["title"] == "Learn Docker"


def test_create_task_without_title(client):
    response = client.post(
        "/api/tasks",
        json={"title": ""}
    )

    assert response.status_code == 400


def test_update_task(client):
    created = client.post(
        "/api/tasks",
        json={"title": "Learn AWS"}
    )

    task_id = created.json["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"status": "Completed"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "Completed"


def test_delete_task(client):
    created = client.post(
        "/api/tasks",
        json={"title": "Learn Linux"}
    )

    task_id = created.json["id"]

    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 200
