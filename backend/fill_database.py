from storage import Storage
from models import Project, Task, Resource

def fill_database():
    db = Storage()

    # Mock data for projects, tasks, and resources
    recipes = [
        {
            "name": "Garlic Shrimp Scampi",
            "description": "A quick and delicious dish where shrimp is sautéed in garlic butter, combined with lemon juice, and served over pasta.",
            "tasks": [
                {"name": "Prepare Ingredients", "description": "Peel and devein shrimp, mince garlic, and prepare lemon juice."},
                {"name": "Cook Shrimp", "description": "Sauté shrimp in garlic butter until pink and cooked through."},
                {"name": "Combine and Serve", "description": "Add lemon juice to the shrimp, toss with cooked pasta, and serve."}
            ],
            "resources": [
                {"name": "Shrimp", "description": "Fresh shrimp, peeled and deveined."},
                {"name": "Garlic", "description": "Minced garlic for flavor."},
                {"name": "Lemon", "description": "Fresh lemon juice for tanginess."},
                {"name": "Pasta", "description": "Cooked pasta to serve with the shrimp."}
            ]
        },
        {
            "name": "Caprese Salad",
            "description": "A simple and refreshing salad made with layers of tomatoes, mozzarella, and basil, drizzled with olive oil.",
            "tasks": [
                {"name": "Slice Ingredients", "description": "Slice tomatoes and mozzarella into even pieces."},
                {"name": "Assemble Salad", "description": "Layer tomatoes, mozzarella, and basil leaves on a plate."},
                {"name": "Drizzle Olive Oil", "description": "Drizzle olive oil over the salad and season with salt and pepper."}
            ],
            "resources": [
                {"name": "Tomatoes", "description": "Fresh, ripe tomatoes."},
                {"name": "Mozzarella", "description": "Fresh mozzarella cheese."},
                {"name": "Basil", "description": "Fresh basil leaves."},
                {"name": "Olive Oil", "description": "Extra virgin olive oil for drizzling."}
            ]
        },
        {
            "name": "Egg Fried Rice",
            "description": "A quick and easy dish where rice is stir-fried with eggs, soy sauce, and vegetables.",
            "tasks": [
                {"name": "Prepare Ingredients", "description": "Chop vegetables and beat eggs."},
                {"name": "Cook Eggs", "description": "Scramble eggs in a hot pan and set aside."},
                {"name": "Stir-Fry Rice", "description": "Stir-fry rice with vegetables and soy sauce, then mix in the eggs."}
            ],
            "resources": [
                {"name": "Rice", "description": "Cooked rice, preferably day-old."},
                {"name": "Eggs", "description": "Beaten eggs for scrambling."},
                {"name": "Vegetables", "description": "Chopped vegetables like carrots, peas, and green onions."},
                {"name": "Soy Sauce", "description": "Soy sauce for seasoning."}
            ]
        }
    ]

    # Add projects, tasks, and resources to the database
    for recipe in recipes:
        project = Project(name=recipe["name"], description=recipe["description"])
        project = db.add(project)

        # Add tasks
        for task_data in recipe["tasks"]:
            task = Task(name=task_data["name"], description=task_data["description"], project_id=project.id)
            db.add(task)

        # Add resources
        for resource_data in recipe["resources"]:
            resource = Resource(name=resource_data["name"], description=resource_data["description"], project_id=project.id)
            db.add(resource)

    print("Database has been populated with mock data.")

if __name__ == "__main__":
    fill_database()