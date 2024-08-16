from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f'<Task {self.id}: {self.done}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)
    
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
