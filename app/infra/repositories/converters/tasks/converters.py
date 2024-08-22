from domain.entities.tasks import Task
from domain.values.tasks import Title, TaskBody, Importance, TimeToComplete
from infra.db.models.task import Tasks


def convert_task_db_model_to_entity(task: Tasks) -> Task:
    return Task(
        oid=task.id,
        title=Title(task.title),
        task_body=TaskBody(task.task_body),
        importance=Importance(task.importance),
        time_to_complete=TimeToComplete(task.time_to_complete),
        user_oid=task.user_id,
        is_completed=task.is_completed
    )
