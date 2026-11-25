from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class EmployeeRole(str, Enum):
    CEO = "CEO"
    PROJECT_MANAGER = "Project Manager"
    UI_DESIGNER = "UI Designer"
    REACT_ARCHITECT = "React Architect"
    FRONTEND_DEVELOPER = "Frontend Developer"
    VISUAL_REVIEWER = "Visual & UX Reviewer"
    FILE_INTEGRITY_SPECIALIST = "File Integrity Specialist"
    QA_TESTER = "QA Tester"
    DOCUMENTATION_WRITER = "Documentation Writer"

class Employee(BaseModel):
    id: str
    name: str
    role: EmployeeRole
    status: str = "idle"
    current_task: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Project(BaseModel):
    id: str
    name: str
    description: str
    client_request: str
    status: ProjectStatus = ProjectStatus.PENDING
    autonomous_mode: bool = True
    human_review_required: bool = False
    pages: List[str] = []
    architecture: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    workspace_path: Optional[str] = None
    metadata: Dict[str, Any] = {}

class Task(BaseModel):
    id: str
    project_id: str
    title: str
    description: str
    assigned_to: EmployeeRole
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = []
    output: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class Message(BaseModel):
    id: str
    project_id: str
    from_agent: str
    to_agent: Optional[str] = None
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class ProjectRequest(BaseModel):
    description: str
    name: Optional[str] = None
    requirements: Optional[str] = None
    autonomous_mode: bool = True