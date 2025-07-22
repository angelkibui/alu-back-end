#!/usr/bin/python3
"""
Retrieve and export ALL employees' TODO lists to a single JSON file.
"""

import json
from urllib.error import HTTPError
from urllib.request import urlopen


def fetch_all_employees_todos():
    """
    Fetch all employees and their TODO lists, then export to JSON.

    Returns:
        dict: Dictionary containing all employees' tasks
    """
    base_url = "https://jsonplaceholder.typicode.com"
    users_url = "{}/users".format(base_url)
    todos_url = "{}/todos".format(base_url)
    all_data = {}

    try:
        # Fetch all users
        with urlopen(users_url) as response:
            users = json.loads(response.read().decode("utf-8"))

        # Fetch all todos
        with urlopen(todos_url) as response:
            todos = json.loads(response.read().decode("utf-8"))

        # Organize todos by user ID
        for user in users:
            user_id = user.get("id")
            username = user.get("username")
            user_todos = [todo for todo in todos if todo.get("userId") == user_id]
            
            tasks_list = []
            for todo in user_todos:
                tasks_list.append({
                    "username": username,
                    "task": todo.get("title", "Untitled Task"),
                    "completed": todo.get("completed", False)
                })
            
            all_data[str(user_id)] = tasks_list

        # Export to JSON file
        with open("todo_all_employees.json", "w") as jsonfile:
            json.dump(all_data, jsonfile, indent=4)

        return all_data

    except HTTPError as http_err:
        print("HTTP Error: {}".format(http_err))
        sys.exit(1)
    except Exception as err:
        print("Error: {}".format(err))
        sys.exit(1)


if __name__ == "__main__":
    fetch_all_employees_todos()
