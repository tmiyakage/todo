from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

JSON_FILE_PATH = 'todos.json'

def load_todos():
    try:
        with open(JSON_FILE_PATH, 'r') as json_file:
            todos = json.load(json_file)
    except FileNotFoundError:
        todos = []
    return todos

def save_todos(todos):
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(todos, json_file, indent=2)

@app.route('/')
def index():
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    new_todo = request.form.get('new_todo')
    todos = load_todos()
    todos.append({'task': new_todo, 'status': '未完了'})
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/update_status/<int:todo_id>/<status>')
def update_status(todo_id, status):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos[todo_id]['status'] = status
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        del todos[todo_id]
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/update_order', methods=['POST'])
def update_order():
    new_order = request.json.get('new_order')
    todos = load_todos()

    # リクエストで受け取った新しい順序にToDoアイテムを更新
    updated_todos = [todos[index] for index in new_order]

    # 保存
    save_todos(updated_todos)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
