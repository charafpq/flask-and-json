from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Text, nullable=True)

@app.route('/')
def hello_start():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        data = request.get_json()
        new_task = Task(name=data["taskName"], desc=data["taskDesc"])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"status": "success"}), 201
        

    return render_template("add.html")

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_task(id):
    task = db.get_or_404(Task, id)
    if request.method == "POST":
        data = request.get_json()
        task.name = data["taskName"]
        task.desc = data["taskDesc"]
        db.session.commit()
        return jsonify({"status": "success"}), 200
    return render_template("edit.html", task=task)

@app.route('/delete/<int:id>', methods=["POST"])
def delete_task(id):
    task = db.get_or_404(Task, id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)