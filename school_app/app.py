from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database for demonstration
students = []

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        students.append({'name': name, 'grade': grade})
        return redirect(url_for('index'))
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)
