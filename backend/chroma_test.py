from vector_store import VectorStore
import unittest
from models import Project, Task, Resource, deserialize_json

class VectorStoreTests(unittest.TestCase):
    store = VectorStore()
    
    def test_can_retrieve_item(self) -> None:
        query = "Salad"
        items = list(self.store.find_items(query))
        self.assertIsNotNone(items)
        
        for json, i_type in items:
            if i_type == Task.__name__:
                data = deserialize_json(json, Task)
                self.assertIsNotNone(data)
            elif i_type == Project.__name__:
                data = deserialize_json(json, Project)
                self.assertIsNotNone(data)
            elif i_type == Resource.__name__:
                data = deserialize_json(json, Resource)
                self.assertIsNotNone(data)
            else:
                print(json)
                raise ValueError(f"Unknown item type {i_type}")
            
if __name__ == '__main__':
    unittest.main()            
            