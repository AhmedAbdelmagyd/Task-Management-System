import pickle
from datetime import datetime, timedelta
import os

# Task class
class Task:
    def __init__(self, title, description, due_date, category):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category

    def __repr__(self):
        return f"Task(title={self.title}, due_date={self.due_date}, category={self.category})"

    def is_due(self):
        return self.due_date <= datetime.now()

# Category class
class Category:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category(name={self.name})"

# User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(username={self.username})"

    def authenticate(self, password):
        return self.password == password

# TaskManager class
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.categories = []
        self.users = []
        self.current_user = None

    def add_task(self, title, description, due_date, category_name):
        category = next((c for c in self.categories if c.name == category_name), None)
        if not category:
            raise ValueError(f"Category {category_name} does not exist.")
        task = Task(title, description, due_date, category)
        self.tasks.append(task)

    def add_category(self, name):
        self.categories.append(Category(name))

    def register_user(self, username, password):
        if any(u.username == username for u in self.users):
            raise ValueError(f"User {username} already exists.")
        self.users.append(User(username, password))

    def authenticate_user(self, username, password):
        user = next((u for u in self.users if u.username == username), None)
        if user and user.authenticate(password):
            self.current_user = user
            return True
        return False

    def list_tasks(self):
        return [task for task in self.tasks if not task.is_due()]

    def list_due_tasks(self):
        return [task for task in self.tasks if task.is_due()]

    def save_data(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_data(cls, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return cls()

# Usage Example
if __name__ == "__main__":
    # Initialize the TaskManager
    task_manager = TaskManager()

    # Register a user
    task_manager.register_user("john_doe", "password123")

    # Authenticate user
    if task_manager.authenticate_user("john_doe", "password123"):
        print("User authenticated successfully.")

    # Add categories
    task_manager.add_category("Work")
    task_manager.add_category("Personal")

    # Add tasks
    task_manager.add_task("Complete project report", "Finish the report by the end of the week", datetime.now() + timedelta(days=2), "Work")
    task_manager.add_task("Buy groceries", "Purchase groceries for the week", datetime.now() + timedelta(days=1), "Personal")

    # List tasks
    print("Upcoming tasks:")
    for task in task_manager.list_tasks():
        print(task)

    # List due tasks
    print("Due tasks:")
    for task in task_manager.list_due_tasks():
        print(task)

    # Save data
    task_manager.save_data("task_manager.pkl")

    # Load data
    loaded_task_manager = TaskManager.load_data("task_manager.pkl")
    print("Loaded tasks:")
    for task in loaded_task_manager.list_tasks():
        print(task)
