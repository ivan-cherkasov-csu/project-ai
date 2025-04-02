import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage import Storage
from models import Project, Task, Resource, ChartQuery
from agent import Agent
from util import init_model

app = FastAPI()
storage = Storage()

chat_agent_context = """You are an assistant for question-answering tasks.
        Use following documents to answer the question.
        If you don't know the answer, just say that you don't know.
        Use three sentences maximum and keep the answer concise:"""
        
chat_agent = Agent(llm=init_model(), system=chat_agent_context)

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
    return storage.getProjects()

@app.get("/tasks", response_model=list[Task])
async def get_tasks() -> list[Task]:
    return storage.getTasks()

@app.get("/resources")
async def get_resources():
    return storage.getResources()

@app.get("/project/tasks/{project_id}", response_model=list[Task])
async def get_project_tasks(project_id: int) -> list[Task]:
    return storage.getProjectTasks(project_id)

@app.post("/project", response_model=Project)
async def add_project(project: Project) -> Project:
    storage.addProject(project)
    return project
    
@app.post("/task", response_model=Task)
async def add_task(task: Task) -> Task:
    storage.addTask(task)
    return task

@app.post("/resource", response_model=Resource)
async def add_resource(resource: Resource) -> Resource:
    storage.addResource(resource)
    return resource

@app.patch("/project", response_model=Project)
async def update_project(project: Project) -> Project:
    storage.updateProject(project)
    return project

@app.patch("/task", response_model=Task)
async def update_task(task: Task) -> Task:
    storage.updateTask(task)
    return task

@app.patch("/resource", response_model=Task)
async def update_resource(task: Task) -> Task:
    storage.updateResource(task)
    return task

@app.delete("/project", response_model=Project)
async def delete_project(project: Project) -> Project:
    storage.deleteProject(project)
    return project

@app.delete("/task", response_model=Task)
async def delete_project(task: Task) -> Task:
    storage.deleteProject(task)
    return task

@app.delete("/resource", response_model=Resource)
async def delete_project(resource: Resource) -> Resource:
    storage.deleteProject(resource)
    return resource

@app.post("/chat", response_model=ChartQuery)
async def chart_query(prompt: ChartQuery) -> ChartQuery:
    prompt.answer = chat_agent.run({"query": prompt.query})
    return prompt