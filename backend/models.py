from pydantic import BaseModel
import json
from typing import Generic, TypeVar, Type
from enum import Enum 

T = TypeVar('T', 'Project', 'Task', 'Resource')
    
def deserialize_json(json_string: str, data_type: Type[T]) -> T:
    data = json.loads(json_string)
    return data_type.model_validate(data)

class ChartQuery(BaseModel, Generic[T]):
    query: str
    attached: T|None = None
    answer: str | None = None
    
class ChatResponse(BaseModel, Generic[T]):
    answer: str 
    projects: list['Project'] = []
    tasks: list['Task'] = []
    resources: list['Resource'] = []
    
    
class ProjectPrompt(BaseModel):
    prompt: str
    project: 'Project'
    
class TaskPrompt(BaseModel):
    prompt: str
    task: 'Task'

class ResourcePrompt(BaseModel):
    prompt: str
    resource: 'Resource'

class Resource(BaseModel):
    id: int | None = None
    name: str
    project_id: int 
    description: str = ""

    class Config:
        from_attributes = True

class Priority(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL= "CRITICAL"

class Task(BaseModel):
    id: int | None = None
    name: str
    project_id: int
    description: str = ""
    acceptance_criteria: str = ""
    priority: Priority = Priority.NORMAL
    
    class Config:
        from_attributes = True

class Project(BaseModel):
    id: int | None = None
    name: str
    description: str = ""
    tasks: list[Task] = []
    resources: list[Resource] = []
    
    class Config:
        from_attributes = True