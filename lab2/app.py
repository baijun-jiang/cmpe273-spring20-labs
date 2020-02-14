from flask import Flask, escape, request, Response

import json

app = Flask(__name__)

students = []
classez = []
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/students', methods=['GET', 'POST'])
def studets():
    if request.method == 'GET':
        id = int(request.args.get('id'))

        if id < len(students):
            return students[id - 1].return_as_payload()
        else:
            return f'cannot find student with id {id}'
    
    if request.method == 'POST':
        new_id = len(students)
        payload = request.get_json()
        students.append(Student(new_id, payload.get('name')))

        return students[new_id].return_as_payload(), 201


@app.route('/classes', methods=['GET', 'POST', 'PATCH'])
def classes():
    if request.method == 'GET':
        id = int(request.args.get('id'))

        if id < len(classez):
            return classez[id - 1].return_as_payload(), 200
    
    if request.method == 'POST':
        new_id = len(classez)
        payload = request.get_json()
        classez.append(Class(new_id, payload.get('name')))

        return classez[new_id].return_as_payload(), 201

    
    if request.method == 'PATCH':
        id = int(request.args.get('id'))

        if id < len(classez):
            class_obj = classez[id]
            student_id = int(request.args.get('sid'))
            class_obj.add_student(students[student_id])
            classez[id] = class_obj
        
        return class_obj.return_as_payload(), 201

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def return_as_payload(self):
        return {'id': self.id, 'name': self.name}

class Class:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.students = []
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def add_student(self, student):
        self.students.append({"student": student.return_as_payload()})
    
    def return_as_payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'students': self.students
        }
