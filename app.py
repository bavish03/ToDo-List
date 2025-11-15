import json
import os
from datetime import datetime
from operator import attrgetter
FILE_NAME = 'data.json'

class Task:
    def __init__(self, name, priority="Medium", completed=False, created_date=None):
        self.name = name
        self.priority = priority
        self.completed = completed
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        status = "[DONE]" if self.completed else "[ ]"
        priority_label = f"(P: {self.priority:<6})"
        return f"{status} {priority_label} {self.name} (Created: {self.created_date[:10]})"

    def mark_complete(self):
        self.completed = True

    def toggle_complete(self):
        self.completed = not self.completed

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON saving."""
        return {
            'name': self.name,
            'priority': self.priority,
            'completed': self.completed,
            'created_date': self.created_date
        }

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
            return

        try:
            with open(FILE_NAME, 'r') as f:
                data = json.load(f)
                self.tasks = [Task(**task_dict) for task_dict in data]
            print(f"Loaded {len(self.tasks)} tasks.")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading tasks: {e}. Starting with empty list.")

    def save_tasks(self):
        data_to_save = [task.to_dict() for task in self.tasks]
        try:
            with open(FILE_NAME, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print("Tasks saved successfully!")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, name, priority):
        new_task = Task(name, priority)
        self.tasks.append(new_task)
        print(f"\nTask '{name}' added with priority '{priority}'.")

    def display_tasks(self, task_list=None):
        if task_list is None:
            task_list = self.tasks

        if not task_list:
            print("\nList is empty or filter returned no results.")
            return

        print("\n--- Current To-Do List ---")
        for index, task in enumerate(task_list):
            print(f"{index + 1}. {task}")
        print("--------------------------")
        
        return task_list

    def filter_tasks(self, criterion):
        
        if criterion.lower() == 'all':
            return self.tasks
        
        elif criterion.lower() in ['low', 'medium', 'high']:
            filtered_list = [t for t in self.tasks if t.priority.lower() == criterion.lower()]
            print(f"\n--- Filtered by Priority: {criterion.upper()} ---")
            
        elif criterion.lower() == 'pending':
            filtered_list = [t for t in self.tasks if not t.completed]
            print("\n--- Filtered: Pending Tasks Only ---")
            
        elif criterion.lower() == 'done':
            filtered_list = [t for t in self.tasks if t.completed]
            print("\n--- Filtered: Completed Tasks Only ---")
            
        else:
            print("Invalid filter criterion. Options: All, Low, Medium, High, Pending, Done.")
            return []
            
        return filtered_list

    def sort_tasks(self, key='created_date', reverse=False):
        try:
            self.tasks.sort(key=attrgetter(key), reverse=reverse)
            print(f"\nTasks sorted by {key} (Reverse: {reverse}).")
        except AttributeError:
            print(f"\nInvalid sorting key: {key}. Defaulting to creation date.")
            self.tasks.sort(key=attrgetter('created_date'))
            
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            print(f"\nTask '{removed_task.name}' deleted.")
        else:
            print("\nError: Task number is out of range.")
            
    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle_complete()
            status = "DONE" if self.tasks[index].completed else "PENDING"
            print(f"\nTask '{self.tasks[index].name}' status set to {status}.")
        else:
            print("\nError: Task number is out of range.")

def get_task_index(manager, prompt="Enter the number of the task: "):
    manager.display_tasks()
    if not manager.tasks:
        return -1
    
    try:
        task_num = input(prompt)
        index = int(task_num) - 1 
        if 0 <= index < len(manager.tasks):
            return index
        else:
            print("\nError: Task number is out of range.")
            return -1
    except ValueError:
        print("\nError: Please enter a valid number.")
        return -1
    
def main():
    manager = TaskManager()

    while True:
        print("\n=============================================")
        print("          ADVANCED TO-DO LIST MANAGER")
        print("=============================================")
        print("1. View Tasks (Master List)")
        print("2. Add New Task")
        print("3. Sort Tasks")
        print("4. Filter Tasks")
        print("5. Toggle Task Status (Complete/Pending)")
        print("6. Delete Task")
        print("7. Exit (and Save)")
        print("=============================================")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            manager.display_tasks()
            
        elif choice == '2':
            name = input("Enter task name: ")
            priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
            if priority not in ['Low', 'Medium', 'High']:
                priority = 'Medium'
            manager.add_task(name, priority)

        elif choice == '3':
            sort_key = input("Sort by: 'name', 'priority', or 'created_date'? (Default: created_date): ") or 'created_date'
            is_reverse = input("Reverse order? (y/n): ").lower() == 'y'
            manager.sort_tasks(key=sort_key, reverse=is_reverse)
            manager.display_tasks()

        elif choice == '4':
            filter_crit = input("Filter by (Low, Medium, High, Pending, Done, All): ").strip().capitalize()
            filtered_list = manager.filter_tasks(filter_crit)
            manager.display_tasks(filtered_list)

        elif choice == '5':
            index = get_task_index(manager, "Enter the number of the task to toggle status: ")
            if index != -1:
                manager.toggle_task(index)

        elif choice == '6':
            index = get_task_index(manager, "Enter the number of the task to DELETE: ")
            if index != -1:
                manager.delete_task(index)

        elif choice == '7':
            manager.save_tasks() 
            print("Application closed. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()