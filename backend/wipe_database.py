from storage import Storage
from models import Project, Task, Resource

def wipe_database():
    db = Storage()

    # Delete all tasks
    tasks = db.get_all(Task)
    for task in tasks:
        db.delete(task)

    # Delete all resources
    resources = db.get_all(Resource)
    for resource in resources:
        db.delete(resource)

    # Delete all projects
    projects = db.get_all(Project)
    for project in projects:
        db.delete(project)

    print("All data has been wiped from the database.")

if __name__ == "__main__":
    wipe_database()