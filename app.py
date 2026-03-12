
from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

@app.route('/')
def home():
    return "Welcome to the Student Grade API!"

@app.route('/student')
def get_student():
    grade = int(request.args.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"

    return jsonify({
        "name": "Your Name",
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

@app.route('/students')
def list_students():
    return jsonify(students)

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
    '''
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    if grade < 0 or grade > 100:
        return jsonify({"error": "Grade must be between 0 and 100"}), 400

    new_student = {
        "id": len(students) + 1,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    })

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
