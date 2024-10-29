from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'XXXXXX'
app.config['MYSQL_DB'] = 'school_db'

mysql = MySQL(app)


# Student class to represent a student object
class Student:
    def __init__(self, id, name, grade):
        self.id = id
        self.name = name
        self.grade = grade


@app.route('/')
def index():
    search_query = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if search_query:
        cursor.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{search_query}%",))
    else:
        cursor.execute("SELECT * FROM students")

    student_tuples = cursor.fetchall()
    cursor.close()

    # Convert tuples to Student objects
    students = [Student(id=row[0], name=row[1], grade=row[2]) for row in student_tuples]

    return render_template('index.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", (name, grade))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')


@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        cursor.execute("UPDATE students SET name = %s, grade = %s WHERE id = %s", (name, grade, student_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()

    # Convert the tuple to a Student object
    student_obj = Student(id=student[0], name=student[1], grade=student[2]) if student else None

    return render_template('update_student.html', student=student_obj)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
