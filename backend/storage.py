from sqlalchemy import create_engine, Column, Integer, String, Enum, Engine, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from models import Project, Task, Resource, Priority, deserialize_json, BaseModel
from vector_store import VectorStore
from typing import Generic, TypeVar, Type

Base = declarative_base()
T = TypeVar('T')

class ProjectsTable(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    tasks = relationship('TasksTable', backref='ProjectsTable', lazy=True)
    resources = relationship('ResourcesTable', backref='ProjectsTable', lazy=True)

    def __repr__(self) -> str:
        result = f"id: {self.id}; name: {self.name}; description:{self.description}; tasks:{self.tasks}"
        return result

class TasksTable(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    description = Column(String)
    acceptance_criteria = Column(String)
    priority = Column(Enum(Priority))

class ResourcesTable(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    description = Column(String)

class Storage(object):
    __engine: Engine
    __session: sessionmaker
    __index: VectorStore

    def __init__(self):
        self.__engine = create_engine('sqlite:///mydatabase.db')
        self.__session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__index = VectorStore()

    def addTask(self, task: Task) -> None:
        if not task.project_id: raise ValueError("Task.project_id should be valid int value")
        db_task = TasksTable(**task.model_dump())
        db_task.id = None
        with self.__session() as session:
            session.add(db_task)
            session.commit()
            task.id = db_task.id
            self.__add_to_index(task, task.id)
            return task

    def addProject(self, project: Project) -> Project:
        db_project = ProjectsTable(**project.model_dump())
        db_project.id = None
        with self.__session() as session:
            session.add(db_project)
            session.commit()
            project.id = db_project.id
            self.__add_to_index(project, project.id)
            return project
        
    def addResource(self, resource: Resource) -> None:
        db_resource = ResourcesTable(**resource.model_dump())
        db_resource.id = None
        with self.__session() as session:
            session.add(db_resource)
            session.commit()
            resource.id = db_resource.id
            self.__add_to_index(resource, resource.id)
            return resource

    def getTasks(self) -> list[Task]:
        with self.__session() as session:
            results = session.query(TasksTable).all()
            tasks = []
            for result in results:
                try:
                    task = Task.model_validate(result)
                    tasks.append(task)
                except Exception as e:
                    print(f"id: {result.id}; name: {result.name}; desc: {result.description}")
            return tasks
    
    def getResources(self) -> list[Resource]:
        with self.__session() as session:
            results = session.query(ResourcesTable).all()
            return [Resource.model_validate(result) for result in results]
        
    def getProjects(self) -> list[Project]:
        with self.__session() as session:
            results = session.query(ProjectsTable).all()
            return [Project.model_validate(result) for result in results]
        
    def getProjectTasks(self, project_id: int) -> list[Task]:
        with self.__session() as session:
            results = session.query(TasksTable).filter(TasksTable.project_id == project_id).all()
            tasks = []
            for result in results:
                task = Task.model_validate(result)
                tasks.append(task)
            return tasks
        
    def getProjectResources(self, project_id) -> list[Resource]:
        with self.__session() as session:
            results = session.query(ResourcesTable).filter(ResourcesTable.project_id == project_id).all()
            return [Resource.model_validate(result) for result in results]
        
    def updateTask(self, task: Task) -> None:
        with self.__session() as session:
            db_task = session.query(TasksTable).filter(TasksTable.id == task.id).first()
            if not db_task: return None

            for key, value in task.model_dump(exclude_unset=True).items():
                setattr(db_task, key, value)

            session.add(db_task)
            session.commit()
            self.__update_index(task, task.id)
    
    def updateResource(self, resource: Resource) -> None:
        with self.__session() as session:
            db_resource = session.query(ResourcesTable).filter(ResourcesTable.id == resource.id).first()
            if not db_resource: return None

            for key, value in resource.model_dump(exclude_unset=True).items():
                setattr(db_resource, key, value)

            session.add(db_resource)
            session.commit()
            self.__update_index(resource, resource.id)

    def updateProject(self, project: Project) -> None:
        with self.__session() as session:
            db_project = session.query(ProjectsTable).filter(ProjectsTable.id == project.id).first()
            if not db_project: return None

            for key, value in project.model_dump(exclude_unset=True).items():
                setattr(db_project, key, value)

            session.add(db_project)
            session.commit()
            self.__update_index(project, project.id)

    def deleteTask(self, task: Task) -> None:
        with self.__session() as session:
            db_item = session.query(TasksTable).filter(TasksTable.id == task.id).first()
            if db_item:
                session.delete(db_item)
                session.commit()
                self.__delete_index(task.id, Task)

    def deleteResource(self, resource: Resource) -> None:
        with self.__session() as session:
            db_item = session.query(ResourcesTable).filter(ResourcesTable.id == resource.id).first()
            if db_item:
                session.delete(db_item)
                session.commit()
                self.__delete_index(resource.id, Resource)
    
    def deleteProject(self, project: Project) -> None:
        with self.__session() as session:
            db_items = session.query(TasksTable).filter(TasksTable.project_id == project.id).all()
            for item in db_items:
                session.delete(item)
                session.commit()
                self.__delete_index(item.id, Task)
            db_items = session.query(ResourcesTable).filter(ResourcesTable.project_id == project.id).all()
            for item in db_items:
                session.delete(item)
                session.commit()
                self.__delete_index(item.id, Resource)
            db_item = session.query(ProjectsTable).filter(ProjectsTable.id == project.id).first()
            if db_item:
                session.delete(db_item)
                session.commit()
                self.__delete_index(project.id, Project)
                
    def __add_to_index(self, model: BaseModel, id: int) -> None:
        item_type = type(model).__name__
        uid = f"{item_type}_{id}"
        json = model.model_dump_json()
        self.__index.add_item(json, uid, item_type)
        
    def __update_index(self, model: BaseModel, id: int) -> None:
        item_type = type(model).__name__
        uid = f"{item_type}_{id}"
        json = model.model_dump_json()
        self.__index.update_item(json, uid, item_type)
    
    def __delete_index(self, id: int, data_type: Type[T]) -> None:
        item_type = data_type.__name__
        uid = f"{item_type}_{id}"
        self.__index.delete_item(uid)
        
    def __find(self, query:str, data_type: Type[T]) -> list[T]:
        item_type = data_type.__name__
        items = self.__index.find_items(query, item_type)
        result = []
        for json, t in items:
            item = deserialize_json(json, data_type)
            result.append(item)
        return result