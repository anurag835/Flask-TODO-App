from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'key'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title = request.form.get('title')
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo item deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
