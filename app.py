from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    user = db.Column(db.String(100))
    status = db.Column(db.String(100))
    severity = db.Column(db.String(100))
    workspace = db.Column((db.String(100)))
    channel = db.Column(db.String(100))

    def __init__(self, name, description, user, status, severity, workspace, channel):
        self.name = name
        self.description = description
        self.user = user
        self.status = status
        self.severity = severity
        self.workspace = workspace
        self.channel = channel


# Product Schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'name', 'description', 'user',
            'status', 'severity', 'workspace', 'channel'
        )


# Init schema
todo_schema = TodoSchema(strict=True)
todos_schema = TodoSchema(many=True, strict=True)


# Create
@app.route('/todo', methods=['POST'])
def add_todo():

    name = request.json['name']
    description = request.json['description']
    user = request.json['user']
    status = request.json['status']
    severity = request.json['severity']
    workspace = request.json['workspace']
    channel = request.json['channel']

    new_todo = Todo(name, description, user, status, severity, workspace, channel)

    db.session.add(new_todo)
    db.session.commit()

    return todo_schema.jsonify(new_todo)


# Get All
@app.route('/todo', methods=['GET'])
def get_todos():

    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result.data)


# Get Single
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):

    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)


@app.route('/your_todos', methods=['GET'])
def testing_my_view():

    print(request.args)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
