from fastapi import APIRouter, Depends, HTTPException, Response
from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/project",
    tags=["Project"],
    description="Creates a project.",
    response_model=schemas.Project,
)
async def create_project_route(
    project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    new_project = crud.create_project(db, project)
    return new_project


@router.get(
    "/projects",
    response_model=list[schemas.Project],
    tags=["Project"],
    description="Returns all projects.",
)
async def read_projects_route(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = crud.read_projects(db, skip, limit)
    if projects is None:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects


@router.get(
    "/project/{id}",
    response_model=schemas.Project,
    tags=["Project"],
    description="Returns a project by it's id.",
)
async def read_project_route(id: int, db: Session = Depends(get_db)):
    project = crud.read_project(db, id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get(
    "/project/developer/{developer_id}",
    response_model=list[schemas.Project],
    tags=["Project"],
    description="Returns all project belonging to the specified developer.",
)
async def read_project_developer_route(
    developer_id: int, db: Session = Depends(get_db)
):
    projects = crud.read_project_developer(db, developer_id)
    return projects


@router.put("/project/{project_id}", tags=["Project"], description="Edits a project.")
async def update_project_route(
    project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    crud.update_project(db, project_id, project)
    return Response(status_code=204)


@router.post(
    "/project/{project_id}/task",
    response_model=schemas.Task,
    tags=["Task"],
    description="Creates a task in a project.",
)
async def create_project_task_route(
    project_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    task = crud.create_task(db, project_id, task)
    return task


@router.get(
    "/project/{project_id}/task/{task_id}",
    response_model=schemas.Task,
    tags=["Task"],
    description="Returns a task in a project.",
)
async def read_project_task_route(
    project_id: int, task_id: int, db: Session = Depends(get_db)
):
    task = crud.read_task(db, project_id, task_id)
    return task


@router.get(
    "/project/{project_id}/tasks",
    response_model=list[schemas.Task],
    tags=["Task"],
    description="Returns all tasks in a project.",
)
async def read_project_tasks_route(project_id: int, db: Session = Depends(get_db)):
    tasks = crud.read_project_tasks(db, project_id)
    return tasks


@router.delete(
    "/project/{project_id}/task/{task_id}",
    tags=["Task"],
    description="Deletes a task in a project.",
)
async def delete_project_task_route(
    project_id: int, task_id: int, db: Session = Depends(get_db)
):
    crud.delete_task(db, project_id, task_id)
    return Response(status_code=204)


@router.post(
    "/project/{project_id}/assignment",
    response_model=schemas.Assignment,
    tags=["Assignment"],
    description="Creates an assignment (proposition of developer to assign to tasks).",
)
async def create_project_assignment_route(
    project_id: int, db: Session = Depends(get_db)
):
    result = crud.create_assignment(db, project_id)
    return result


@router.get(
    "/project/{project_id}/assignment/{assignment_id}",
    response_model=schemas.Assignment,
    tags=["Assignment"],
    description="Get an assignment in a project.",
)
async def read_project_assignment_route(
    project_id: int, assignment_id: int, db: Session = Depends(get_db)
):
    result = crud.read_assignment(db, project_id, assignment_id)
    return result


@router.put(
    "/project/{project_id}/assignment/{assignment_id}",
    tags=["Assignment"],
    description="Edits an assignment in a project.",
)
async def update_assignment_route(
    project_id: int,
    assignment_id: int,
    assignment: schemas.AssignmentUpdate,
    db: Session = Depends(get_db),
):
    crud.update_assignment(db, project_id, assignment_id, assignment)
    return Response(status_code=200)


@router.delete(
    "/project/{project_id}/assignment/{assignment_id}",
    tags=["Assignment"],
    description="Deletes an assignment in a project.",
)
async def delete_project_assignment_route(
    project_id: int, assignment_id: int, db: Session = Depends(get_db)
):
    crud.delete_assignment(db, project_id, assignment_id)
    return Response(status_code=200)


@router.get(
    "/project/{project_id}/assignments",
    tags=["Assignment"],
    description="Returns all assignments in project.",
)
async def read_project_assignments_route(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.read_project_assignments(db, project_id)


@router.put(
    "/project/{project_id}/task/{task_id}",
    tags=["Task"],
    description="Edits a task in a project.",
)
async def update_project_task_route(
    project_id: int,
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    task = crud.update_task(db, project_id, task_id, task)
    return task


@router.delete("/project/{id}", tags=["Project"], description="Deletes a project.")
async def delete_project_route(id: int, db: Session = Depends(get_db)):
    crud.delete_project(db, id)
    return Response(status_code=200)
