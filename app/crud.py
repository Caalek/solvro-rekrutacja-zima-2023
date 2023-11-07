from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from .database import SessionLocal
from . import models, schemas


# DEVELOPER
def create_developer(db: Session, developer: schemas.DeveloperCreate):
    new_developer = models.Developer(**developer.model_dump())
    db.add(new_developer)
    db.commit()
    db.refresh(new_developer)
    return new_developer


def read_developer(db: Session, id: int):
    developer = db.query(models.Developer).filter(models.Developer.id == id).first()
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer


def read_developers(db: Session, skip: int, limit: int):
    developers = db.query(models.Developer).offset(skip).limit(limit).all()
    if len(developers) == 0:
        raise HTTPException(status_code=404, detail="No developers found")


def update_developer(db: Session, id: int, developer: schemas.DeveloperUpdate):
    existing_developer = (
        db.query(models.Developer).filter(models.Developer.id == id).first()
    )
    if existing_developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    for field, value in developer.model_dump(exclude_unset=True).items():
        setattr(existing_developer, field, value)
    db.add(existing_developer)
    db.commit()
    db.refresh(existing_developer)
    return existing_developer


def delete_developer(db: Session, id: int):
    db.query(models.Developer).filter(models.Developer.id == id).delete()
    db.query(models.ProjectDeveloper).filter(
        models.ProjectDeveloper.developer_id == id
    ).delete()
    db.commit()


# PROJECT
def create_project(db: Session, project: schemas.ProjectCreate):
    new_project = models.Project(
        developer_owner_id=project.developer_owner_id, name=project.name
    )
    db.add(new_project)
    db.flush()
    for developer_id in project.developers:
        developer = (
            db.query(models.Developer)
            .filter(models.Developer.id == developer_id)
            .first()
        )
        if developer is None:
            raise HTTPException(
                status_code=400, detail="All developers of the project must exist"
            )
        db.add(
            models.ProjectDeveloper(
                developer_id=developer.id, project_id=new_project.id
            )
        )
    db.commit()
    return {
        "id": new_project.id,
        "developer_owner_id": project.developer_owner_id,
        "name": project.name,
        "developers": project.developers
    }


def read_project(db: Session, id: int):
    basic_info = db.query(models.Project).filter(models.Project.id == id).first()
    if basic_info is None:
        raise HTTPException(status_code=404, detail="Project not found")
    response = {
        "id": basic_info.id,
        "developer_owner_id": basic_info.developer_owner_id,
        "name": basic_info.name,
    }
    developer_id_rows = (
        db.query(models.ProjectDeveloper)
        .filter(models.ProjectDeveloper.project_id == id)
        .all()
    )
    developer_ids = []
    for row in developer_id_rows:
        developer_ids.append(row.developer_id)
        response["developers"] = developer_ids
    response["developers"] = developer_ids
    return response


def read_project_developer(db: Session, developer_id: int):
    project_id_rows = (
        db.query(models.Project)
        .filter(models.Project.developer_owner_id == developer_id)
        .all()
    )
    if len(project_id_rows) == 0:
        raise HTTPException(status_code=404, detail="This developer has no projects")
    response = []
    for row in project_id_rows:
        db = SessionLocal()
        response.append(read_project(db=db, id=row.id))
    return response


def read_projects(db: Session, skip: int, limit: int):
    projects_no_developers = db.query(models.Project).offset(skip).limit(limit).all()
    response = []
    for project in projects_no_developers:
        db = SessionLocal()
        response.append(read_project(db, project.id))
    return response


def update_project(db: Session, project_id: int, project: schemas.ProjectUpdate):
    existing_project = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in project.model_dump(exclude_unset=True).items():
        setattr(existing_project, field, value)
    db.query(models.ProjectDeveloper).filter(
        models.ProjectDeveloper.project_id == project_id
    ).delete()
    for developer_id in project.developers:
        new_entry = models.ProjectDeveloper(
            developer_id=developer_id, project_id=project_id
        )
        db.add(new_entry)
    db.add(existing_project)
    db.commit()


def delete_project(db: Session, id: int):
    db.query(models.Project).filter(models.Project.id == id).delete()
    db.query(models.ProjectDeveloper).filter(
        models.ProjectDeveloper.project_id == id
    ).delete()
    db.commit()


# TASK
def create_task(db: Session, project_id: int, task: schemas.TaskCreate):
    if task.developer_id:  # jeśli przypisano kogoś do taska
        new_task = models.Task(
            name=task.name,
            project_id=project_id,
            state="IN_PROGRESS",
            estimation=task.estimation,
            specialization=task.specialization,
            developer_id=task.developer_id,
            datetime_assigned=datetime.utcnow(),
        )
    else:
        new_task = models.Task(
            name=task.name,
            project_id=project_id,
            estimation=task.estimation,
            specialization=task.specialization,
        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def read_task(db: Session, project_id: int, task_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.project_id == project_id)
        .filter(models.Task.id == task_id)
        .first()
    )


def read_project_tasks(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def update_task(db: Session, project_id: int, task_id: int, task: schemas.TaskUpdate):
    existing_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .filter(models.Task.project_id == project_id)
        .first()
    )
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task.model_dump(exclude_unset=True).items():
        setattr(existing_task, field, value)
    db.add(existing_task)
    db.commit()
    db.refresh(existing_task)
    return existing_task


def delete_task(db: Session, project_id: int, task_id: int):
    db.query(models.Task).filter(models.Task.id == task_id).filter(
        models.Task.project_id == project_id
    ).delete()
    db.commit()


# ASSIGNMENT
def create_assignment(db: Session, project_id: int):
    all_project_tasks = (
        db.query(models.Task).filter(models.Task.project_id == project_id).all()
    )
    completed_project_tasks = [
        task for task in all_project_tasks if task.state == "CLOSED"
    ]
    uncompleted_project_tasks = [
        task for task in all_project_tasks if task.state == "NOT_ASSIGNED"
    ]
    if not uncompleted_project_tasks:
        raise HTTPException(
            status_code=400, detail="There are no tasks with state NOT_ASSIGNED"
        )
    developer_ids_query = (
        db.query(models.ProjectDeveloper)
        .filter(models.ProjectDeveloper.project_id == project_id)
        .all()
    )
    developer_ids = [row.developer_id for row in developer_ids_query]
    developers = (
        db.query(models.Developer).filter(models.Developer.id.in_(developer_ids)).all()
    )
    assignments = {}
    for d_id in developer_ids:
        assignments[d_id] = []

    def find_fastest_developer(developer_ids, estimation):
        average = 99999999
        fastest_developer_id = -1
        for dev_id in developer_ids:
            sum_seconds = 0
            developer_tasks_estimation = []
            for t in completed_project_tasks:
                if t.developer_id == dev_id and t.estimation == estimation:
                    developer_tasks_estimation.append(t)
            if len(developer_tasks_estimation) == 0:
                print(f"NO DATA FOR DEV {dev_id} ESTIMATION {estimation} ")
                continue
            for task in developer_tasks_estimation:
                sum_seconds += (
                    task.datetime_completed - task.datetime_assigned
                ).total_seconds()
            current_average = sum_seconds / len(developer_tasks_estimation)
            print(
                f"DEV {dev_id} FOR ESTIMATION {estimation} AVERAGE TIME {current_average}"
            )
            if current_average < average:
                average = current_average
                fastest_developer_id = dev_id
        return fastest_developer_id

    for specialization in ["FRONTEND", "BACKEND", "UX/UI", "DEVOPS"]:
        print(f"SPECIALIZATION {specialization}")
        developer_ids_in_specialization = [
            d.id for d in developers if d.specialization == specialization
        ]
        tasks_in_specialization = [
            t for t in uncompleted_project_tasks if t.specialization == specialization
        ]
        leftover_tasks = []
        developer_total_estimation = {}
        for d in developer_ids_in_specialization:
            developer_total_estimation[d] = 0

        for task in tasks_in_specialization:
            print(f"TASK {task.id} ESTIMATION {task.estimation}")
            print(f"DEVELOPERS: {[i for i in developer_ids_in_specialization ]}")
            # szukamy najszybszego historyczne deva do takiego zadania
            developer_id = find_fastest_developer(
                developer_ids_in_specialization, task.estimation
            )
            if developer_id != -1:
                assignments[developer_id].append(task)
                developer_total_estimation[developer_id] += task.estimation
                print(f"ASSIGNING TASK {task.id} TO DEV {developer_id}")
            else:
                leftover_tasks.append(task)

        # jeśli nie mamy danych na temat czasów tego konkretnego deva i tej estymacji, to
        # zawsze dodajemy temu, kto ma najmniej estymacji
        if leftover_tasks:
            while len(leftover_tasks) > 0:
                task = leftover_tasks.pop()
                for developer_id in developer_ids_in_specialization:
                    if developer_total_estimation[developer_id] == min(
                        developer_total_estimation.values()
                    ):
                        assignments[developer_id].append(task)
                        break

    response = {}
    response["changes"] = {}
    for d_id in developer_ids:
        response["changes"][int(d_id)] = []
    for key, value in assignments.items():
        for task in value:
            response["changes"][key].append(task.id)
    assignment = models.Assignment(project_id=project_id)
    db.add(assignment)
    db.flush()
    response["id"] = assignment.id
    for developer_id, task_ids in response["changes"].items():
        for task_id in task_ids:
            change = models.ProposedChange(
                developer_id=developer_id, task_id=task_id, assignment_id=assignment.id
            )
            db.add(change)
    db.commit()
    return response


def read_assignment(db: Session, project_id: int, assignment_id: int):
    response = {"changes": {}}
    assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == assignment_id)
        .filter(models.Assignment.project_id == project_id)
        .first()
    )
    changes = (
        db.query(models.ProposedChange)
        .filter(models.ProposedChange.assignment_id == assignment_id)
        .all()
    )
    for change in changes:
        if change.developer_id not in response["changes"].keys():
            response["changes"][change.developer_id] = [change.task_id]
        else:
            response["changes"][change.developer_id].append(change.task_id)
    response["accepted"] = assignment.accepted
    response["id"] = assignment_id
    return response


def read_project_assignments(db: Session, project_id: int):
    response = []
    assignments = (
        db.query(models.Assignment)
        .filter(models.Assignment.project_id == project_id)
        .all()
    )
    if assignments is None or len(assignments) == 0:
        raise HTTPException(
            status_code=404, detail="There are no assignments in this project."
        )
    for a in assignments:
        response.append(read_assignment(db, project_id, a.id))
    return response


def update_assignment(
    db: Session, project_id: int, assignment_id: int, assignment: schemas.TaskUpdate
):
    existing_assignment = (
        db.query(models.Assignment)
        .filter(models.Assignment.id == assignment_id)
        .filter(models.Assignment.project_id == project_id)
        .first()
    )
    if existing_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for field, value in assignment.model_dump(exclude_unset=True).items():
        setattr(existing_assignment, field, value)

    if assignment.accepted:
        changes = (
            db.query(models.ProposedChange)
            .filter(models.ProposedChange.assignment_id == assignment_id)
            .all()
        )
        for change in changes:
            update_task(
                db,
                project_id,
                change.task_id,
                schemas.TaskUpdate(
                    developer_id=change.developer_id,
                    datetime_assigned=datetime.utcnow(),
                    state="IN_PROGRESS",
                ),
            )
    else:
        db.query(models.ProposedChange).filter(
            models.ProposedChange.assignment_id == assignment_id
        ).delete()
        db.commit()


def delete_assignment(db: Session, project_id: int, assignment_id: int):
    db.query(models.Assignment).filter(
        models.Assignment.project_id == project_id
    ).filter(models.Assignment.id == assignment_id).delete()
    db.query(models.ProposedChange).filter(
        models.ProposedChange.assignment_id == assignment_id
    ).delete()
    db.commit()
