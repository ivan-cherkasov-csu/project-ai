from sqlalchemy import create_engine, Column, Integer, String, Enum, Engine, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from models import Project, Task, Resource, Priority, BaseModel, T
from vector_store import VectorStore, Iterable
from typing import List, Union, TypeVar, Type

Base = declarative_base()

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
        
    def index(self) -> VectorStore: return self.__index

    def addTask(self, task: Task) -> None:
        if not task.project_id: raise ValueError("Task.project_id should be valid int value")
        db_task = TasksTable(**task.model_dump())
        db_task.id = None
        with self.__session() as session:
            session.add(db_task)
            session.commit()
            task.id = db_task.id
            self.__index.add_item(task)
            return task

    def addProject(self, project: Project) -> Project:
        db_project = ProjectsTable(**project.model_dump())
        db_project.id = None
        with self.__session() as session:
            session.add(db_project)
            session.commit()
            project.id = db_project.id
            self.__index.add_item(project)
            return project
        
    def addResource(self, resource: Resource) -> None:
        db_resource = ResourcesTable(**resource.model_dump())
        db_resource.id = None
        with self.__session() as session:
            session.add(db_resource)
            session.commit()
            resource.id = db_resource.id
            self.__index.add_item(resource)
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
            self.__index.update_item(task)
    
    def updateResource(self, resource: Resource) -> None:
        with self.__session() as session:
            db_resource = session.query(ResourcesTable).filter(ResourcesTable.id == resource.id).first()
            if not db_resource: return None

            for key, value in resource.model_dump(exclude_unset=True).items():
                setattr(db_resource, key, value)

            session.add(db_resource)
            session.commit()
            self.__index.update_item(resource)

    def updateProject(self, project: Project) -> None:
        with self.__session() as session:
            db_project = session.query(ProjectsTable).filter(ProjectsTable.id == project.id).first()
            if not db_project: return None

            for key, value in project.model_dump(exclude_unset=True).items():
                setattr(db_project, key, value)

            session.add(db_project)
            session.commit()
            self.__index.update_item(project)

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
                
    def find_item_type(self, query: str, item_type: Type[T]) -> List[T]:
        items = self.__index.find_items(query, item_type)
        result = list(items)
        if item_type == Project:
            for item in result:
                item.tasks = self.getProjectTasks(item.id)
                item.resources = self.getProjectResources(item.id)
        return result
    
    def run(self, query: str) -> List[Union[Project, Task, Resource]]: return self.find_items(query)
    
    def find_items(self, query: str) -> List[Union[Project, Task, Resource]]:
        items = self.__index.find(query)
        result = []
        for item in items:
            if item is Project:
                item = self.rehydrate_project(item)
            result.append(item)
        return result
        
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
    
    def __delete_index(self, id: int, data_type: Type[T]) -> None:
        item_type = data_type.__name__
        uid = f"{item_type}_{id}"
        self.__index.delete_item(uid)
        
    def rehydrate_project(self, item: Project) -> Project:
        item.tasks = self.getProjectTasks(item.id)
        item.resources = self.getProjectResources(item.id)
        return item