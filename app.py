from flask import Flask, jsonify, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODEL
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    section = db.Column(db.String(100))

# CREATE DB
with app.app_context():
    db.create_all()


# 🏠 HOME
@app.route('/')
def home():
    return redirect(url_for('student_ui'))


# 📋 UI
@app.route('/ui')
def student_ui():
    students = Student.query.all()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Students</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <div class="container mt-5">

        <h1 class="mb-4 text-center">🎓 Student Management</h1>

        <div class="mb-3 text-end">
            <a href="/add_student_form" class="btn btn-success">➕ Add Student</a>
        </div>

        <table class="table table-bordered table-hover shadow bg-white">
            <thead class="table-dark">
                <tr>
                    <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {% for s in students %}
                <tr>
                    <td>{{s.id}}</td>
                    <td>{{s.name}}</td>
                    <td>
                        <span class="badge bg-{{'success' if s.grade >= 75 else 'danger'}}">
                            {{s.grade}}
                        </span>
                    </td>
                    <td>{{s.section}}</td>
                    <td>
                        <a href="/edit/{{s.id}}" class="btn btn-warning btn-sm">Edit</a>
                        <a href="/delete/{{s.id}}" class="btn btn-danger btn-sm">Delete</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <div class="text-center mt-4">
            <a href="/summary" class="btn btn-info">📊 View Summary (JSON)</a>
        </div>

    </div>
    </body>
    </html>
    '''
    return render_template_string(html, students=students)


# ➕ ADD FORM
@app.route('/add_student_form')
def add_student_form():
    html = '''
    <div class="container mt-5">
        <h2>Add Student</h2>
        <form method="POST" action="/add_student" class="card p-4 shadow">
            <input class="form-control mb-3" name="name" placeholder="Name" required>
            <input class="form-control mb-3" name="grade" type="number" placeholder="Grade" required>
            <input class="form-control mb-3" name="section" placeholder="Section" required>
            <button class="btn btn-success">Save</button>
            <a href="/ui" class="btn btn-secondary">Back</a>
        </form>
    </div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    '''
    return render_template_string(html)


# ➕ CREATE
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    if grade < 0 or grade > 100:
        return "Grade must be between 0 and 100"

    new_student = Student(name=name, grade=grade, section=section)
    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('student_ui'))


# ✏️ EDIT FORM
@app.route('/edit/<int:id>')
def edit_student_form(id):
    student = Student.query.get_or_404(id)

    html = '''
    <div class="container mt-5">
        <h2>Edit Student</h2>
        <form method="POST" action="/update/{{student.id}}" class="card p-4 shadow">
            <input class="form-control mb-3" name="name" value="{{student.name}}" required>
            <input class="form-control mb-3" name="grade" type="number" value="{{student.grade}}" required>
            <input class="form-control mb-3" name="section" value="{{student.section}}" required>
            <button class="btn btn-primary">Update</button>
            <a href="/ui" class="btn btn-secondary">Back</a>
        </form>
    </div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    '''
    return render_template_string(html, student=student)


# ✏️ UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    student = Student.query.get_or_404(id)

    student.name = request.form.get("name")
    student.grade = int(request.form.get("grade"))
    student.section = request.form.get("section")

    db.session.commit()
    return redirect(url_for('student_ui'))


# ❌ DELETE
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('student_ui'))


# 📊 SUMMARY
@app.route('/summary')
def summary():
    students = Student.query.all()

    grades = [s.grade for s in students]

    if not grades:
        return jsonify({"message": "No data"})

    avg = sum(grades) / len(grades)
    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed

    return jsonify({
        "average_grade": avg,
        "passed": passed,
        "failed": failed
    })


if __name__ == '__main__':
    app.run(debug=True)
