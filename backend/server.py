import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools import get_rag_tool, get_search_tool, Storage
from models import Project, Task, Resource, ChartQuery, ChatResponse
from agent import Agent

app = FastAPI()
storage = Storage()

chat_agent_context = """You are an assistant for project management tasks.
        You can use tools and attached items if any to answer.
        If you don't know the answer, just say that you don't know."""
        
chat_agent = Agent(model_name='qwen2.5', system=chat_agent_context,tools=[get_search_tool(), get_rag_tool(Storage())])

origins = [
    "http://localhost:5173"  # Allow all paths for this origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the origins list
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Hello world!"}

@app.get("/projects", response_model=list[Project])
async def get_projects() -> list[Project]:
    return storage.get_all(Project)

@app.get("/tasks", response_model=list[Task])
async def get_tasks() -> list[Task]:
    return storage.get_all(Task)

@app.get("/resources", response_model=list[Resource])
async def get_resources() -> list[Resource]:
    return storage.get_all(Resource)

@app.get("/tasks/{project_id}", response_model=list[Task])
async def get_project_tasks(project_id: int) -> list[Task]:
    return storage.get_by_project(Task, project_id)

@app.post("/project", response_model=Project)
async def add_project(project: Project) -> Project:
    return storage.add(project)
    
@app.post("/task", response_model=Task)
async def add_task(task: Task) -> Task:
    return storage.add(task)

@app.post("/resource", response_model=Resource)
async def add_resource(resource: Resource) -> Resource:
    return storage.add(resource)

@app.patch("/project", response_model=Project)
async def update_project(project: Project) -> Project:
    storage.update(project)
    return project

@app.patch("/task", response_model=Task)
async def update_task(task: Task) -> Task:
    storage.update(task)
    return task

@app.patch("/resource", response_model=Resource)
async def update_resource(resource: Resource) -> Resource:
    storage.update(resource)
    return resource

@app.delete("/project", response_model=Project)
async def delete_project(project: Project) -> Project:
    storage.delete(project)
    return project

@app.delete("/task", response_model=Task)
async def delete_task(task: Task) -> Task:
    storage.delete(task)
    return task

@app.delete("/resource", response_model=Resource)
async def delete_resource(resource: Resource) -> Resource:
    storage.delete(resource)
    return resource

@app.post("/chat", response_model=ChatResponse)
async def chart_query(prompt: ChartQuery) -> ChartQuery:
    prompt.answer = chat_agent.run(prompt)
    return prompt