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

class Storage:
    __engine: Engine
    __session: sessionmaker
    __index: VectorStore

    def __init__(self):
        self.__engine = create_engine('sqlite:///mydatabase.db')
        self.__session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__index = VectorStore()

    def index(self) -> VectorStore:
        return self.__index

    def add(self, item: T) -> T:
        table = self.__get_table(item)
        if isinstance(item, Task) and item.project_id is None:
            raise ValueError("Task must have a project_id")
        if isinstance(item, Resource) and item.project_id is None:
            raise ValueError("Resource must have a project_id")
        db_item = table(**item.model_dump())
        with self.__session() as session:
            session.add(db_item)
            session.commit()
            item.id = db_item.id
            self.__index.add_item(item)
            return item

    def get_all(self, item_type: Type[T]) -> List[T]:
        table = self.__get_table(item_type)
        with self.__session() as session:
            results = session.query(table).all()
            return [item_type.model_validate(result) for result in results]

    def get_by_project(self, item_type: Type[T], project_id: int) -> List[T]:
        table = self.__get_table(item_type)
        with self.__session() as session:
            results = session.query(table).filter(table.project_id == project_id).all()
            return [item_type.model_validate(result) for result in results]

    def update(self, item: T) -> None:
        table = self.__get_table(item)
        with self.__session() as session:
            db_item = session.query(table).filter(table.id == item.id).first()
            if not db_item:
                return None
            for key, value in item.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            session.add(db_item)
            session.commit()
            self.__index.update_item(item)

    def delete(self, item: T) -> None:
        table = self.__get_table(item)
        if isinstance(item, Project):
            for task in item.tasks:
                self.delete(task)
            for resource in item.resources:
                self.delete(resource)
        with self.__session() as session:
            db_item = session.query(table).filter(table.id == item.id).first()
            if db_item:
                session.delete(db_item)
                session.commit()
                self.__delete_index(item.id, type(item))

    def __get_table(self, item_or_type: Union[T, Type[T]]) -> Type:
        if isinstance(item_or_type, Project) or item_or_type == Project:
            return ProjectsTable
        elif isinstance(item_or_type, Task) or item_or_type == Task:
            return TasksTable
        elif isinstance(item_or_type, Resource) or item_or_type == Resource:
            return ResourcesTable
        raise ValueError(f"Unsupported type: {item_or_type}")
    
    def find_item_type(self, query: str, item_type: Type[T]) -> List[T]:
        items = self.__index.find_items(query, item_type)
        result = list(items)
        if item_type == Project:
            for item in result:
                self.__rehydrate_project(item)
        return result
    
    def run(self, query: str) -> List[Union[Project, Task, Resource]]: return self.find_items(query)
    
    def find_items(self, query: str) -> List[Union[Project, Task, Resource]]:
        items = self.__index.find(query)
        result = []
        for item in items:
            if item is Project:
                item = self.__rehydrate_project(item)
            result.append(item)
        return result

    def __delete_index(self, id: int, data_type: Type[T]) -> None:
        item_type = data_type.__name__
        uid = f"{item_type}_{id}"
        self.__index.delete_item(uid)
        
    def __rehydrate_project(self, item: Project) -> Project:
        item.tasks = self.get_by_project(Task, item.id)
        item.resources = self.get_by_project(Resource, item.id)
        return item