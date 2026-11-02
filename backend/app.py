
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage
tasks = []
next_id = 1


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "TaskFlow API is running!",
        "status": "success"
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": next_id,
        "title": title,
        "priority": data.get("priority", "Medium"),
        "status": data.get("status", "Pending")
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks

    task = next(
        (t for t in tasks if t["id"] == task_id),
        None
    )

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)

    return jsonify({"message": "Task deleted successfully"})


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next(
        (t for t in tasks if t["id"] == task_id),
        None
    )

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "status" in data:
        task["status"] = data["status"]

    if "priority" in data:
        task["priority"] = data["priority"]

    return jsonify(task)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
