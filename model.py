# model.py

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def add_course(self, course):
        self.courses[course.course_id] = course


class Course:
    def __init__(self, course_id, title):
        self.course_id = course_id
        self.title = title
        self.assessments = []

    def add_assessment(self, assessment):
        self.assessments.append(assessment)


class Assessment:
    def __init__(self, title, score):
        self.title = title
        self.score = score
