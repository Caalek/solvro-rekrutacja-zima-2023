from pydantic import BaseModel, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class Specialization(str, Enum):
    FRONTEND = "FRONTEND"
    BACKEND = "BACKEND"
    DEVOPS = "DEVOPS"
    UX_UI = "UX/UI"


class TaskState(str, Enum):
    CLOSED = "CLOSED"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_ASSIGNED = "NOT_ASSIGNED"


class Developer(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: Specialization


class DeveloperCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: Specialization


class DeveloperUpdate(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    specialization: Specialization = Field(default=None)


class Task(BaseModel):
    id: int
    name: str
    project_id: int
    state: TaskState
    created_at: datetime
    estimation: int
    specialization: Specialization
    developer_id: Optional[int] = Field(default=None)
    date_assigned: datetime = Field(default=None)
    date_completed: datetime = Field(default = None)


class TaskCreate(BaseModel):
    name: str
    estimation: int
    specialization: Specialization
    developer_id: int = Field(default=None)

    @validator("estimation")
    def check_if_fibonacci(value_checked):
        if value_checked == 0 or value_checked == 1:
            return True
        n1 = 1
        n2 = 2
        while True:
            value = n1 + n2
            if value == value_checked:
                return value_checked
            elif value > value_checked:
                raise ValueError(
                    "Estimation must be a number from the Fibonacci sequence"
                )
            n1 = n2
            n2 = value


class TaskUpdate(BaseModel):
    name: str = Field(default=None)
    project_id: int = Field(default=None)
    state: TaskState = Field(default=None)
    estimation: int = Field(default=None)
    specialization: Specialization = Field(default=None)
    developer_id: int = Field(default=None)
    date_assigned: int = Field(default=None)
    date_completed: int = Field(default=None)


class Project(BaseModel):
    id: int
    name: str
    developer_owner_id: int
    developers: list[int]


class ProjectCreate(BaseModel):
    name: str
    developer_owner_id: int
    developers: list[int]

class ProjectUpdate(BaseModel):
    name: str = Field(default=None)
    developer_owner_id: int = Field(default=None)
    developers: list[int] = Field(default=None)


class AssignmentUpdate(BaseModel):
    accepted: bool 

class Assignment(BaseModel):
    id: int
    accepted: Optional[bool] = Field(default=None)
    changes: dict[int, list[int]]


