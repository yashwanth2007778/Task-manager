# Smart Task Management System

## Live Demo
https://task-manager-goz1.onrender.com

## GitHub Repository
https://github.com/yashwanth2007778/Task-manager

---

# Project Overview

Smart Task Management System is a Flask-based web application that helps users manage daily tasks efficiently.

The project includes:
- User Authentication
- REST APIs
- PostgreSQL Database
- Task Analytics using Pandas & NumPy
- Real-Time Updates using WebSockets
- Responsive Frontend using Bootstrap

---

# Features

## Authentication
- User Registration
- User Login
- Logout

## Task Management
- Add Task
- Edit Task
- Delete Task
- Complete Task

## Analytics
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage

## Real-Time Updates
Implemented using Flask-SocketIO.

## REST APIs
- GET /api/tasks
- POST /api/add_task
- PUT /api/complete/<id>
- DELETE /api/delete/<id>

---

# Technologies Used

- Python
- Flask
- PostgreSQL
- Pandas
- NumPy
- Flask-SocketIO
- Bootstrap
- HTML/CSS

---

# Project Structure

Task-manager/
│
├── app.py
├── requirements.txt
├── schema.sql
├── render.yaml
├── README.md
│
├── templates/
├── static/
├── models/
├── routes/

---

# Installation Steps

## Clone Repository

```bash
git clone https://github.com/yashwanth2007778/Task-manager.git
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

---

# Database Schema

The project uses PostgreSQL database with:
- users table
- tasks table

Schema is available in:
schema.sql

---

# Author

Yashwanth