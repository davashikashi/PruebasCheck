from locust import HttpUser, task, between
from dotenv import load_dotenv
import os
from faker import Faker
import random

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

fake = Faker()

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    host = os.getenv("BACKEND_URL")  # Obtener la URL del backend desde las variables de entorno

    @task
    def create_project_success(self):
        project_data = {
            "asignatureName": fake.word(),
            "img": fake.image_url(),
            "tasks": []
        }
        response = self.client.post("/projects", json=project_data)
        if response.status_code == 201:
            print(f"Success: Project created successfully: {response.status_code}")
        else:
            print(f"Failure: Failed to create project: {response.status_code}, {response.text}")

    @task
    def create_project_failure(self):
        project_data = {
            "asignatureName": "",  # Datos inválidos
            "img": fake.image_url(),
            "tasks": []
        }
        response = self.client.post("/projects", json=project_data)
        if response.status_code == 400:
            print(f"Success: Caught expected validation error: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior: {response.status_code}, {response.text}")

    @task
    def update_project(self):
        project_id = random.randint(1, 1000)  # ID aleatorio
        data_scenario = random.choice(["missing_field", "extra_field", "normal"])
        
        if data_scenario == "missing_field":
            project_data = {
                "img": fake.image_url(),
                "tasks": []
            }
        elif data_scenario == "extra_field":
            project_data = {
                "asignatureName": fake.word(),
                "img": fake.image_url(),
                "tasks": [],
                "extraField": "extra"
            }
        else:
            project_data = {
                "asignatureName": fake.word(),
                "img": fake.image_url(),
                "tasks": []
            }

        response = self.client.patch(f"/projects/{project_id}", json=project_data)
        if response.status_code in [200, 400, 404]:
            print(f"Success: Project update tested with {data_scenario}: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior during project update with {data_scenario}: {response.status_code}, {response.text}")

    @task
    def delete_project_error(self):
        project_id = random.randint(1, 10000)  # ID válido para probar el error
        response = self.client.delete(f"/projects/{project_id}")
        if response.status_code == 500:
            print(f"Success: Internal server error handled: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior: {response.status_code}, {response.text}")

    @task
    def create_task_success(self):
        task_data = {
            "taskName": fake.word(),
            "description": fake.text(),
            "checkBox": False,
            "fechaInicio": fake.date_time().isoformat(),
            "fechaFinal": fake.date_time().isoformat(),
            "projectId": random.randint(1, 100)  # Utilizar IDs aleatorios para pruebas ficticias
        }
        response = self.client.post("/tasks", json=task_data)
        if response.status_code == 201:
            print(f"Success: Task created successfully: {response.status_code}")
        else:
            print(f"Failure: Failed to create task: {response.status_code}, {response.text}")

    @task
    def create_task_failure(self):
        task_data = {
            "description": fake.text(),
            "checkBox": False,
            "fechaInicio": fake.date_time().isoformat(),
            "fechaFinal": fake.date_time().isoformat(),
            "projectId": random.randint(1, 100)  # Utilizar IDs aleatorios para pruebas ficticias
        }
        response = self.client.post("/tasks", json=task_data)
        if response.status_code == 400:
            print(f"Success: Caught expected validation error: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior: {response.status_code}, {response.text}")

    @task
    def update_task(self):
        task_id = random.randint(1, 1000)  # ID aleatorio
        data_scenario = random.choice(["missing_field", "extra_field", "normal"])
        
        if data_scenario == "missing_field":
            task_data = {
                "description": fake.text()
            }
        elif data_scenario == "extra_field":
            task_data = {
                "taskName": fake.word(),
                "description": fake.text(),
                "extraField": "extra"
            }
        else:
            task_data = {
                "taskName": fake.word(),
                "description": fake.text()
            }

        response = self.client.patch(f"/tasks/{task_id}", json=task_data)
        if response.status_code in [200, 400, 404]:
            print(f"Success: Task update tested with {data_scenario}: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior during task update with {data_scenario}: {response.status_code}, {response.text}")

    @task
    def delete_task_error(self):
        task_id = random.randint(1, 100)
        response = self.client.delete(f"/tasks/{task_id}")
        if response.status_code == 500:
            print(f"Success: Internal server error handled: {response.status_code}")
        else:
            print(f"Failure: Unexpected behavior: {response.status_code}, {response.text}")


    # @task
    # def delete_projects(self):
    #     start_project_id = 532  # Proyecto inicial en el rango
    #     end_project_id = 2309   # Proyecto final en el rango

    #     for project_id in range(start_project_id, end_project_id + 1):
    #         self.client.delete(f"/projects/{project_id}")
           