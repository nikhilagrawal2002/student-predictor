
from flask import Flask, render_template, request, redirect
import matplotlib.pyplot as plt
import io
import base64
import csv
from predictor import predict_grade

app = Flask(__name__)
DATA_FILE = "data/students.csv"

def load_students():
    students = []
    try:
        with open(DATA_FILE, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # ⬅️ Skip the header row
            for row in reader:
                if row:
                    name, course, *scores = row
                    scores = list(map(int, scores))
                    predicted = predict_grade(scores)
                    students.append((name, course, scores, predicted))
    except FileNotFoundError:
        pass
    return students

    students = []
    try:
        with open(DATA_FILE, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    name, course, *scores = row
                    scores = list(map(int, scores))
                    predicted = predict_grade(scores)
                    students.append((name, course, scores, predicted))
    except FileNotFoundError:
        pass
    return students

def save_student(name, course, scores):
    with open(DATA_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, course] + scores)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"].strip()
        course = request.form["course"].strip()
        scores_input = request.form["scores"].strip()

        if name and course and scores_input:
            try:
                scores = list(map(int, scores_input.split(",")))
                save_student(name, course, scores)
                return redirect("/students")
            except ValueError:
                return render_template("index.html", error="Please enter valid numeric scores.")
    return render_template("index.html")

@app.route("/students")
def students():
    student_data = load_students()
    return render_template("student_list.html", students=student_data)

@app.route("/dashboard")
def dashboard():
    students = load_students()
    total_students = len(students)
    if total_students > 0:
        avg_pred = round(sum(s[3] for s in students) / total_students, 2)
    else:
        avg_pred = 0

    # Calculate number of students per course
    course_counts = {}
    for _, course, _, _ in students:
        course_counts[course] = course_counts.get(course, 0) + 1

    return render_template("dashboard.html", total_students=total_students, avg_pred=avg_pred, course_counts=course_counts)
@app.route("/graph")
def graph():
    students = load_students()

    fig, ax = plt.subplots()
    for name, _, scores, _ in students:
        ax.plot(range(1, len(scores)+1), scores, marker='o', label=name)

    ax.set_title("Student Performance Over Assessments")
    ax.set_xlabel("Assessment Number")
    ax.set_ylabel("Score")
    ax.legend()
    ax.grid(True)

    # Save plot to a string buffer
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return render_template("graph.html", image=image_base64)

if __name__ == "__main__":
    app.run(debug=True)
