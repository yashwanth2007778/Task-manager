
from flask import Flask, render_template, request, redirect, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
import psycopg2
import pandas as pd
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = "secretkey"

# PostgreSQL Connection
conn = psycopg2.connect(
    host="dpg-d881i1ojo6nc73d2io00-a.oregon-postgres.render.com",
    user="postgresql_f0ut_user",
    password="xWJ34DZe1hfGJltFw0Of6DJwmwuxQfmx",
    database="postgresql_f0ut",
    port="5432"
)

cur = conn.cursor()

# Create Table
cur.execute("""

CREATE TABLE IF NOT EXISTS tasks (

    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    priority VARCHAR(50),
    status VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

# Create Users Table
cur.execute("""

CREATE TABLE IF NOT EXISTS users (

    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL

)

""")

conn.commit()
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        password = generate_password_hash(
            request.form['password']
        )

        query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        """

        cur.execute(query, (username, password))

        conn.commit()

        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        query = """
        SELECT * FROM users
        WHERE username=%s
        """

        cur.execute(query, (username,))

        user = cur.fetchone()

        if user and check_password_hash(user[2], password):

            session['user'] = username

            flash("Login Successful!", "success")

            return redirect('/')

        else:

            flash("Invalid Username or Password", "danger")

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')
# Home Page

@app.route('/')
def index():

    if 'user' not in session:
        return redirect('/login')

    cur.execute("SELECT * FROM tasks ORDER BY id DESC")

    tasks = cur.fetchall()

    # Analytics using Pandas & NumPy

    df = pd.DataFrame(tasks, columns=[
        "id",
        "title",
        "description",
        "priority",
        "status",
        "created_date"
    ])

    total_tasks = len(df)

    completed_tasks = np.sum(
        df['status'].str.lower() == 'completed'
    )

    pending_tasks = np.sum(
        df['status'].str.lower() == 'pending'
    )

    completion_percentage = 0

    if total_tasks > 0:

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            2
        )

    return render_template(

        'index.html',

        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=completion_percentage

    )

# Add Task
@app.route('/add', methods=['POST'])
def add_task():

    title = request.form['title']

    description = request.form['description']

    priority = request.form['priority']

    query = """

    INSERT INTO tasks
    (title, description, priority, status)

    VALUES (%s, %s, %s, %s)

    """

    values = (
        title,
        description,
        priority,
        "Pending"
    )

    cur.execute(query, values)

    conn.commit()

    socketio.emit('task_update', {
        'message': 'New task added'
    })

    return redirect('/')
    # Edit Task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']

        query = """

        UPDATE tasks
        SET title=%s,
            description=%s,
            priority=%s
        WHERE id=%s

        """

        values = (
            title,
            description,
            priority,
            id
        )

        cur.execute(query, values)

        conn.commit()

        socketio.emit('task_update', {
            'message': 'Task updated'
        })

        return redirect('/')

    query = "SELECT * FROM tasks WHERE id=%s"

    cur.execute(query, (id,))

    task = cur.fetchone()

    return render_template(
        'edit.html',
        task=task
    )
    # Complete Task
@app.route('/complete/<int:id>')
def complete_task(id):

    query = """

    UPDATE tasks
    SET status = %s
    WHERE id = %s

    """

    cur.execute(query, ("Completed", id))

    conn.commit()

    socketio.emit('task_update', {
        'message': 'Task completed'
    })

    return redirect('/')
# Delete Task

@app.route('/delete/<int:id>')
def delete_task(id):

    query = """

    DELETE FROM tasks
    WHERE id = %s

    """

    cur.execute(query, (id,))

    conn.commit()

    socketio.emit('task_update', {
        'message': 'Task deleted'
    })

    return redirect('/')
# API - Get All Tasks
@app.route('/api/tasks')
def api_tasks():

    cur.execute("SELECT * FROM tasks ORDER BY id DESC")

    tasks = cur.fetchall()

    task_list = []

    for task in tasks:

        task_data = {

            "id": task[0],
            "title": task[1],
            "description": task[2],
            "priority": task[3],
            "status": task[4],
            "created_date": str(task[5])

        }

        task_list.append(task_data)

    return jsonify(task_list)


# API - Add Task
@app.route('/api/add_task', methods=['POST'])
def api_add_task():

    data = request.json

    title = data['title']
    description = data['description']
    priority = data['priority']

    query = """

    INSERT INTO tasks
    (title, description, priority, status)

    VALUES (%s, %s, %s, %s)

    """

    values = (
        title,
        description,
        priority,
        "Pending"
    )

    cur.execute(query, values)

    conn.commit()

    return jsonify({
        "message": "Task added successfully"
    })


# API - Complete Task
@app.route('/api/complete/<int:id>', methods=['PUT'])
def api_complete_task(id):

    query = """

    UPDATE tasks
    SET status = %s
    WHERE id = %s

    """

    cur.execute(query, ("Completed", id))

    conn.commit()

    return jsonify({
        "message": "Task completed"
    })


# API - Delete Task
@app.route('/api/delete/<int:id>', methods=['DELETE'])
def api_delete_task(id):

    query = """

    DELETE FROM tasks
    WHERE id = %s

    """

    cur.execute(query, (id,))

    conn.commit()

    return jsonify({
        "message": "Task deleted"
    })
# Run App
if __name__ == '__main__':

    socketio.run(app, host="0.0.0.0", port=5000)


       