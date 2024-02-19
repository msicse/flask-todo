from flask import Flask, render_template, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__, template_folder='templates', static_folder='assets')

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="my_flask_app"
)
cursor = db.cursor()

# Create a table for your data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT
    )
""")
db.commit()

@app.route('/')
def index():
    # Fetch all tasks from the database
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')

    # Insert new task into the database
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    db.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    # Delete task from the database based on ID
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
