from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# 🏠 HOME
@app.route('/')
def home():
    return redirect(url_for('student_ui'))


# 📋 UI: SHOW ALL STUDENTS
@app.route('/ui')
def student_ui():
    html = '''
    <h1>Student List</h1>
    <a href="/add_student_form">Add New Student</a><br><br>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
        </tr>
        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.grade}}</td>
            <td>{{s.section}}</td>
            <td>
                <a href="/edit/{{s.id}}">Edit</a> |
                <a href="/delete/{{s.id}}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, students=students)


# ➕ ADD FORM
@app.route('/add_student_form')
def add_student_form():
    html = '''
    <h2>Add Student</h2>
    <form action="/add_student" method="POST">
        Name: <input type="text" name="name"><br><br>
        Grade: <input type="number" name="grade"><br><br>
        Section: <input type="text" name="section"><br><br>
        <button type="submit">Add Student</button>
    </form>
    <br><a href="/ui">Back</a>
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

    new_student = {
        "id": len(students) + 1,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)
    return redirect(url_for('student_ui'))


# ✏️ EDIT FORM
@app.route('/edit/<int:id>')
def edit_student_form(id):
    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found"

    html = '''
    <h2>Edit Student</h2>
    <form action="/update/{{student.id}}" method="POST">
        Name: <input type="text" name="name" value="{{student.name}}"><br><br>
        Grade: <input type="number" name="grade" value="{{student.grade}}"><br><br>
        Section: <input type="text" name="section" value="{{student.section}}"><br><br>
        <button type="submit">Update</button>
    </form>
    <br><a href="/ui">Back</a>
    '''
    return render_template_string(html, student=student)


# ✏️ UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found"

    student["name"] = request.form.get("name")
    student["grade"] = int(request.form.get("grade"))
    student["section"] = request.form.get("section")

    return redirect(url_for('student_ui'))


# ❌ DELETE
@app.route('/delete/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('student_ui'))


# 📊 SUMMARY API
@app.route('/summary')
def summary():
    grades = [s["grade"] for s in students]

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
