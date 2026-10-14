from flask import Flask, request, jsonify, abort

app = Flask(__name__)

todos = {}
current_id = 1

@app.route('/todos', methods=['POST'])
def create_todo():
    global current_id
    data = request.json
    if not data or 'task' not in data:
        abort(400, 'Task content missing')
    todo = {
        'id': current_id,
        'task': data['task'],
        'completed': False
    }
    todos[current_id] = todo
    current_id += 1
    return jsonify(todo), 201

@app.route('/todos', methods=['GET'])
def list_todos():
    return jsonify(list(todos.values()))

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    if todo_id not in todos:
        abort(404, 'Todo not found')
    data = request.json
    if not data or 'task' not in data:
        abort(400, 'Task content missing')
    todos[todo_id]['task'] = data['task']
    return jsonify(todos[todo_id])

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id not in todos:
        abort(404, 'Todo not found')
    del todos[todo_id]
    return '', 204

@app.route('/todos/<int:todo_id>/complete', methods=['POST'])
def mark_complete(todo_id):
    if todo_id not in todos:
        abort(404, 'Todo not found')
    todos[todo_id]['completed'] = True
    return jsonify(todos[todo_id])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
