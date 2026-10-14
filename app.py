from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory storage for todo items
# Format: {id: {"task": str, "completed": bool}}
todos = {}
next_id = 1

@app.route('/todos', methods=['POST'])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or 'task' not in data:
        abort(400, description="Task is required")
    todo = {"task": data['task'], "completed": False}
    todos[next_id] = todo
    response = {"id": next_id, **todo}
    next_id += 1
    return jsonify(response), 201

@app.route('/todos', methods=['GET'])
def list_todos():
    response = [{"id": _id, **todo} for _id, todo in todos.items()]
    return jsonify(response)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    if todo_id not in todos:
        abort(404, description="Todo item not found")
    data = request.get_json()
    if not data or 'task' not in data:
        abort(400, description="Task is required")
    todos[todo_id]['task'] = data['task']
    response = {"id": todo_id, **todos[todo_id]}
    return jsonify(response)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id not in todos:
        abort(404, description="Todo item not found")
    del todos[todo_id]
    return '', 204

@app.route('/todos/<int:todo_id>/complete', methods=['POST'])
def mark_complete(todo_id):
    if todo_id not in todos:
        abort(404, description="Todo item not found")
    todos[todo_id]['completed'] = True
    response = {"id": todo_id, **todos[todo_id]}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
