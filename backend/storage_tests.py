import unittest
from models import Task, Project, Resource
from storage import Storage

class TestSuit(unittest.TestCase):
    db = Storage()
    def test_can_add_project_to_db(self):
        project = Project(name="Garlic Shrimp Scampi", description="Sauté shrimp in garlic butter, add lemon juice, and serve over pasta.")
        new_project = self.db.addProject(project)
        self.assertEqual(project.id, new_project.id)

    def test_can_add_task_to_db(self):
        project = self.db.addProject(Project(name="Caprese Salad", description="Layer tomatoes, mozzarella, basil, drizzle with olive oil."))
        task = Task(name="Egg Fried Rice", description="Stir-fry rice with eggs, soy sauce, and veggies", project_id=project.id)
        new_task = self.db.addTask(task)
        self.assertEqual(task.id, new_task.id)

    def test_can_add_and_retrieve_project(self):
        project = Project(name="Chicken Caesar Salad", description="Toss grilled chicken, romaine, croutons, Caesar dressing.")
        self.db.addProject(project)
        projects = self.db.getProjects()
        self.assertGreaterEqual(len(projects),1)

    def test_can_retrieve_task_from_db(self):
        project = self.db.addProject(Project(name="Honey Garlic Chicken", description="Pan-fry chicken, glaze with honey, soy sauce, garlic"))
        task = Task(name="Tuna Melts", description="Mix tuna with mayo, spread on bread, top with cheese, broil.", project_id=project.id)
        self.db.addTask(task)
        tasks = self.db.getTasks()
        self.assertGreaterEqual(len(tasks),1)

    def test_can_retrieve_resource_from_db(self):
        project = self.db.addProject(Project(name="Quesadillas", description="Fill tortillas with cheese, beans, veggies, grill until crispy."))
        resource = Resource(name="Spicy Chicken Stir-Fry", description="Sauté chicken, sambal oelek, soy sauce, veggies.", project_id=project.id)
        self.db.addResource(resource)
        resources = self.db.getResources()
        self.assertGreaterEqual(len(resources),1)
    
    def test_can_add_and_update_project(self):
        project = Project(name="Lentil Soup", description="Simmer lentils with onions, carrots, garlic, broth")
        self.db.addProject(project)
        project = self.db.getProjects()[0]
        project.name = "Update Project"
        self.db.updateProject(project)

    def test_can_retrieve_task_and_update(self):
        project = self.db.addProject(Project(name="Tomato Pasta", description="Cook pasta, toss with tomato sauce, garlic, basil."))
        task = Task(name="Salmon & Asparagus", description="Bake salmon, asparagus with olive oil, lemon.", project_id=project.id)
        self.db.addTask(task)
        task = self.db.getTasks()[0]
        task.name = "Updated Task"
        self.db.updateTask(task)
        self.assertIsNotNone(task.project_id)

    def test_can_retrieve_resource_and_update(self):
        project = self.db.addProject(Project(name="Shrimp Tacos", description="Fill tortillas with shrimp, cabbage, lime crema."))
        resource = Resource(name="Tomato Pasta",  project_id=project.id)
        self.db.addResource(resource)
        resource = self.db.getResources()[0]
        resource.name = "Updated Resource"
        self.db.updateTask(resource)
        
    def test_can_retrieve_task_for_project(self):
        project = self.db.addProject(Project(name="Black Bean Burgers", description="Mash beans, mix with breadcrumbs, spices, pan-fry."))
        task = Task(name="Chicken Burritos", description="Wrap chicken, beans, cheese, salsa in tortillas.", project_id=project.id)
        self.db.addTask(task)
        project_tasks = self.db.getProjectTasks(project.id)
        self.assertGreaterEqual(len(project_tasks), 1)
        for t in project_tasks:
            self.db.deleteTask(t)

    def test_can_delete_all_tasks(self):
        tasks = self.db.getTasks()
        for task in tasks:
            self.db.deleteTask(task)
    
    def test_can_delete_all_resources(self):
        resources = self.db.getResources()
        for resource in resources:
            self.db.deleteResource(resource)
    
    def test_can_delete_all_projects(self):
        projects = self.db.getProjects()
        for project in projects:
            self.db.deleteProject(project)

if __name__ == '__main__':
    unittest.main()