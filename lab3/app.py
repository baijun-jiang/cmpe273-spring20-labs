
from ariadne import QueryType, graphql_sync, make_executable_schema, MutationType
from ariadne.constants import PLAYGROUND_HTML

from flask import Flask, escape, request, Response, jsonify
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        self.students.append(student)
    
    def return_as_payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'students': self.students
        }

type_defs = """
    type Query {
        hello: String!
        get_students: [Student!]
        get_student(id:Int!): Student
        get_classes: [Class!]
        get_class(id:Int!): Class
    }

    type Student {
        name: String!
        id: Int!
    }

    type Class {
        id: Int!
        name: String!
        students: [Student]
    }

    type Mutation {
        add_student(name: String!): Student!
        add_class(name: String!): Class!
        register_student(cid: Int!, sid: Int): Class!
    }
"""

query = QueryType()
mutation = MutationType()

@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent

@mutation.field("add_student")
def resolve_add_student(_, info, name):
    new_id = len(students)
    new_student = Student(new_id, name)
    students.append(new_student)
    return new_student

@query.field("get_students")
def resolve_get_students(_, info):
    return students

@query.field("get_student")
def resolve_get_student(_, info, id):
    if id >= len(students) or id < 0:
        return None
    
    return students[id]

@query.field("get_classes")
def reslove_get_classes(_, info):
    return classez

@query.field("get_class")
def reslove_get_class(_, info, id):
    if id >= len(classez) or id < 0:
        return None
    
    return classez[id]

@mutation.field("add_class")
def reslove_add_class(_, info, name):
    new_id = len(classez)
    new_class = Class(new_id, name)
    classez.append(new_class)
    return new_class

@mutation.field("register_student")
def reslove_register_student(_, info, cid, sid):
    if cid < 0 or cid >= len(classez) or sid < 0 or sid >= len(students):
        return None
    clazz = classez[cid]
    student = students[sid]
    clazz.add_student(student)
    classez[cid] = clazz

    return clazz

schema = make_executable_schema(type_defs, [query, mutation])

app = Flask(__name__)

students = []
classez = []


@app.route("/", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)