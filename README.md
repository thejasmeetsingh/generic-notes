# Generic Notes

A simple note management application built with Python3, Django, Django Rest Framework (DRF), and PostgreSQL. The application is containerized with Docker for easy setup and deployment, ensuring compatibility across different platforms. It leverages Gunicorn as the WSGI HTTP Server with Uvicorn workers to handle asynchronous requests efficiently. Also dedicated logger is added to get detail of each request and or any error.

## Features

- **User Management:** Users can sign up and log in to the application.
- **Note Creation:** Authenticated users can create notes.
- **Note Update:** Users can update their notes.
- **Note Sharing:** Users can share notes with other users, granting them view or update access.
- **Version History:** Users can view the version history of a note, tracking changes made, the author of the changes, and the timestamps of those changes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Install [docker](https://www.docker.com/products/docker-desktop/).
2. Clone the repository.
3. Navigate to the project directory.
4. Start the application by running command: `docker-compose up -d`.
5. After the containers are up and running, you can access the API endpoints via `http://localhost:8000`.

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/17396704-f5adf0f8-4c30-42ce-9212-ea179f294826?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17396704-f5adf0f8-4c30-42ce-9212-ea179f294826%26entityType%3Dcollection%26workspaceId%3D392b781a-05ab-415b-9eb8-456aca6f3129)

To run automated tests for the application, execute the command: `docker container exec -it app python manage.py test api.tests`.
