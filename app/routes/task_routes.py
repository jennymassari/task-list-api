from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db


tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    if "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        completed_at = request_body["completed_at"]

    else:
        completed_at = None

    new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=completed_at )
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": check_complete(new_task.completed_at)

    }
    }

    return response, 201

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    tasks = db.session.scalars(query.order_by(Task.id))
    

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
             
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": check_complete(task.completed_at)
                
            }
        )

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    return {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": check_complete(task.completed_at)
                }
            }

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']

    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    else:
        task.completed_at = None

    db.session.commit()

    return {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": check_complete(task.completed_at)
                }
            }

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"}

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task

def check_complete(completed_at):
    if not completed_at:
        return False
    else:
        return True














