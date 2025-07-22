#!/usr/bin/python3
"""
Retrieve and export employee TODO list progress to JSON format.
"""

import json
import sys
from urllib.error import HTTPError
from urllib.request import urlopen


def export_to_json(employee_id, username, todos):
    """
    Export employee TODO list to JSON file.

    Args:
        employee_id (int): Employee ID
        username (str): Employee username
        todos (list): List of todo tasks
    """
    filename = "{}.json".format(employee_id)
    tasks_list = []
    
    for task in todos:
        tasks_list.append({
            "task": task.get("title", "Untitled Task"),
            "completed": task.get("completed", False),
            "username": username
        })
    
    data = {str(employee_id): tasks_list}
    
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)


def get_employee_todo_progress(employee_id):
    """
    Fetch and display TODO list progress for a given employee ID.

    Args:
        employee_id (int): The ID of the employee
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = "{}/users/{}".format(base_url, employee_id)
    todos_url = "{}/users/{}/todos".format(base_url, employee_id)

    try:
        with urlopen(user_url) as response:
            user_data = json.loads(response.read().decode("utf-8"))
            username = user_data.get("username", "Unknown")

        with urlopen(todos_url) as response:
            todos = json.loads(response.read().decode("utf-8"))

        # Export to JSON
        export_to_json(employee_id, username, todos)

        # Display progress (optional)
        done = sum(1 for task in todos if task.get("completed", False))
        print("Employee {} is done with tasks({}/{}):".format(
            username, done, len(todos)))

    except HTTPError as http_err:
        print("HTTP Error: {}".format(http_err))
        sys.exit(1)
    except Exception as err:
        print("Error: {}".format(err))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)
