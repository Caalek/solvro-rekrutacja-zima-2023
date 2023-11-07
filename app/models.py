from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from .database import Base


class Developer(Base):
    __tablename__ = "developer"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    class Config:
        orm_mode = True


class Task(Base):

    def __repr__(self):
        return f"Task(id={self.id}, specialization={self.specialization}, estimation={self.estimation})"
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    state = Column(String, nullable=False, default="NOT_ASSIGNED")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    estimation = Column(Integer, nullable=False)
    specialization = Column(String, nullable=False)
    developer_id = Column(
        Integer, ForeignKey("developer.id"), nullable=True, default=None
    )
    datetime_assigned = Column(DateTime, nullable=True, default=None)
    datetime_completed = Column(DateTime, nullable=True, default=None)


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    developer_owner_id = Column(Integer, ForeignKey("developer.id"), nullable=False)
    name = Column(String, nullable=False)


class ProjectDeveloper(Base):  # przypisanie developera do projektu
    __tablename__ = "project_developer"
    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    developer_id = Column(
        Integer, ForeignKey("developer.id"), nullable=False, index=True
    )
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)


class Assignment(Base):
    __tablename__ = "assignment"
    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    project_id = Column(
        Integer, ForeignKey("project.id"), nullable=False
    )
    accepted = Column(Boolean, default=None, nullable=True) #jak true to wdraża w życie proposed change jak false to usuwa je

class ProposedChange(
    Base
):  # proponowanie przypisania wygenerowane przez algorytm, do zaakceptowania później
    __tablename__ = "proposed_change"
    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=False)
    developer_id = Column(
        Integer, ForeignKey("developer.id"), nullable=False, index=True
    )
    task_id = Column(Integer, nullable=False)
