from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

# Configure database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)

    @property
    def remarks(self):
        return "Pass" if self.grade >= 75 else "Fail"

# Initialize database
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# List all students
@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

# Add new student form
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        grade = int(request.form['grade'])
        section = request.form['section']

        if grade < 0 or grade > 100:
            flash("Grade must be between 0 and 100", "danger")
            return redirect(url_for('add_student'))

        new_student = Student(name=name, grade=grade, section=section)
        db.session.add(new_student)
        db.session.commit()
        flash(f"Student {name} added successfully!", "success")
        return redirect(url_for('list_students'))

    return render_template('add_student.html')

# Update student
@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.grade = int(request.form['grade'])
        student.section = request.form['section']

        if student.grade < 0 or student.grade > 100:
            flash("Grade must be between 0 and 100", "danger")
            return redirect(url_for('update_student', id=id))

        db.session.commit()
        flash(f"Student {student.name} updated successfully!", "success")
        return redirect(url_for('list_students'))

    return render_template('update_student.html', student=student)

# Delete student
@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f"Student {student.name} deleted successfully!", "success")
    return redirect(url_for('list_students'))

# Summary page
@app.route('/summary')
def summary():
    students = Student.query.all()
    if students:
        grades = [s.grade for s in students]
        avg = sum(grades) / len(grades)
        passed = len([g for g in grades if g >= 75])
        failed = len(grades) - passed
    else:
        avg = passed = failed = 0

    return render_template('summary.html', avg=avg, passed=passed, failed=failed)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
