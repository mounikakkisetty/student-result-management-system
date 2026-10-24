
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from contextlib import closing

app = Flask(__name__)

DB_NAME = "students.db"


# Create database and table if they do not exist
def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mark1 REAL NOT NULL,
                mark2 REAL NOT NULL,
                mark3 REAL NOT NULL,
                total REAL NOT NULL,
                average REAL NOT NULL,
                grade TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()


init_db()


# Calculate total, average, grade and pass/fail
def calculate_result(mark1, mark2, mark3):
    marks = [mark1, mark2, mark3]
    total = sum(marks)
    average = total / 3

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 50:
        grade = "C"
    else:
        grade = "Needs Improvement"

    status = "PASS" if all(mark >= 35 for mark in marks) else "FAIL"

    return total, round(average, 2), grade, status


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add a new student result
@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name", "").strip()

    try:
        mark1 = float(request.form.get("mark1", ""))
        mark2 = float(request.form.get("mark2", ""))
        mark3 = float(request.form.get("mark3", ""))
    except ValueError:
        return "Please enter valid numeric marks.", 400

    marks = [mark1, mark2, mark3]

    if not name:
        return "Please enter the student's name.", 400

    if any(mark < 0 or mark > 100 for mark in marks):
        return "Marks must be between 0 and 100.", 400

    total, average, grade, status = calculate_result(*marks)

    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute("""
            INSERT INTO students
            (name, mark1, mark2, mark3, total, average, grade, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, mark1, mark2, mark3,
              total, average, grade, status))
        conn.commit()

    return render_template(
        "result.html",
        name=name,
        marks=marks,
        total=total,
        average=average,
        grade=grade,
        status=status
    )


# Display all saved student records
@app.route("/students")
def students():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.row_factory = sqlite3.Row
        records = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    return render_template("students.html", records=records)


# EDIT: Show existing details and update them
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        try:
            mark1 = float(request.form.get("mark1", ""))
            mark2 = float(request.form.get("mark2", ""))
            mark3 = float(request.form.get("mark3", ""))
        except ValueError:
            return "Please enter valid numeric marks.", 400

        marks = [mark1, mark2, mark3]

        if not name:
            return "Please enter the student's name.", 400

        if any(mark < 0 or mark > 100 for mark in marks):
            return "Marks must be between 0 and 100.", 400

        total, average, grade, status = calculate_result(*marks)

        with closing(sqlite3.connect(DB_NAME)) as conn:
            cursor = conn.execute("""
                UPDATE students
                SET name = ?, mark1 = ?, mark2 = ?, mark3 = ?,
                    total = ?, average = ?, grade = ?, status = ?
                WHERE id = ?
            """, (name, mark1, mark2, mark3, total, average,
                  grade, status, student_id))
            conn.commit()

            if cursor.rowcount == 0:
                return "Student record not found.", 404

        return redirect(url_for("students"))

    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.row_factory = sqlite3.Row
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if student is None:
        return "Student record not found.", 404

    return render_template("edit_student.html", student=student)


# DELETE: Remove one student record
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        conn.commit()

    return redirect(url_for("students"))


if __name__ == "__main__":
    app.run(debug=True)
