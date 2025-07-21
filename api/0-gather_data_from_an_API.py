#!/usr/bin/python3
"""
Script to fetch and display an employee's TODO list progress from a REST API.
"""

import json
import sys
from urllib.error import HTTPError
from urllib.request import urlopen


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays an employee's TODO list progress.

    Args:
        employee_id (int): The ID of the employee.
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    try:
        # Get employee information
        user_url = "{}/users/{}".format(base_url, employee_id)
        with urlopen(user_url) as response:
            user_data = json.loads(response.read().decode('utf-8'))
            employee_name = user_data.get('name', 'Unknown Employee')

        # Get TODO list
        todos_url = "{}/users/{}/todos".format(base_url, employee_id)
        with urlopen(todos_url) as response:
            todos_data = json.loads(response.read().decode('utf-8'))

        # Calculate progress
        total_tasks = len(todos_data)
        done_tasks = sum(1 for task in todos_data if task.get('completed', False))
        done_tasks_titles = [task.get('title', 'Untitled Task') 
                           for task in todos_data if task.get('completed', False)]

        # Display progress
        print("Employee {} is done with tasks({}/{}):".format(
            employee_name, done_tasks, total_tasks))
        for title in done_tasks_titles:
            print("\t {}".format(title))

    except HTTPError as e:
        print("Error fetching data: {}".format(e))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)
