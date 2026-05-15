import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yashwanth2007",
    database="taskdb"
)

cursor = conn.cursor()

while True:

    print("\n========== TASK MANAGER ==========")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task Status")
    print("4. Delete Task")
    print("5. Search Tasks")
    print("6. Exit")

    choice = input("\nEnter choice: ")

    # Add Task
    if choice == "1":

        title = input("Enter title: ")
        description = input("Enter description: ")
        priority = input("Enter priority (High/Medium/Low): ")

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

        cursor.execute(query, values)

        conn.commit()

        print("\nTask added successfully!")

    # View Tasks
    elif choice == "2":

        cursor.execute("""
        SELECT id, title, priority, status, created_date
        FROM tasks
        ORDER BY id DESC
        """)

        tasks = cursor.fetchall()

        print("\n========== TASK LIST ==========")

        for task in tasks:

            print(f"""
ID: {task[0]}
Title: {task[1]}
Priority: {task[2]}
Status: {task[3]}
Created: {task[4]}
-----------------------------
""")

    # Update Task
    elif choice == "3":

        task_id = input("Enter task ID: ")

        status = input(
            "Enter new status (Pending/Completed): "
        )

        query = """
        UPDATE tasks
        SET status = %s
        WHERE id = %s
        """

        cursor.execute(query, (status, task_id))

        conn.commit()

        print("\nTask updated successfully!")

    # Delete Task
    elif choice == "4":

        task_id = input("Enter task ID to delete: ")

        query = """
        DELETE FROM tasks
        WHERE id = %s
        """

        cursor.execute(query, (task_id,))

        conn.commit()

        print("\nTask deleted successfully!")

    # Search Task
    elif choice == "5":

        keyword = input("Enter keyword: ")

        query = """
        SELECT * FROM tasks
        WHERE title LIKE %s
        """

        cursor.execute(query, ('%' + keyword + '%',))

        tasks = cursor.fetchall()

        print("\n========== SEARCH RESULTS ==========")

        for task in tasks:
            print(task)

    # Exit
    elif choice == "6":

        print("\nExiting Task Manager...")
        break

    else:
        print("\nInvalid choice!")

cursor.close()
conn.close()