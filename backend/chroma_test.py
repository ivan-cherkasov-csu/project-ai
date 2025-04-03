from storage import Storage
import unittest
from models import Project, Task

class VectorStoreTests(unittest.TestCase):
    db = Storage()
    
    def test_can_find_and_rehydrate_project(self) -> None:
        query = "Honey Garlic Chicken"
        projects = list(self.db.find_item_type(query, Project))
        result = None
        for project in projects:
            if project.name == query:
                result = project
                
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result.tasks), 1)
    
    def test_can_retrieve_item(self) -> None:
        query = "Salad"
        projects = list(self.db.index().find_items(query, Project))
        self.assertIsNotNone(projects)
        
        for project in projects:
            self.assertIsNotNone(project.id)
            self.assertIsNotNone(project.name)
            self.assertIsNotNone(project.description)
        
    def test_exclude(self) -> None:
        task = Task(name="foo", description="bar", project_id=-1)
        json = task.model_dump_json(exclude={"tasks", "resources"})
        self.assertIsNotNone(json)
            
if __name__ == '__main__':
    unittest.main()            
            