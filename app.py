from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)

class Todo1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project = db.Column(db.String(1000), nullable=False)
    due_date = db.Column(db.String(100), nullable=False)
    usn = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    data = Todo1.query.all()
    context = []
    for dt in data:
        dd = {"id": dt.id, "usn": dt.usn, "name": dt.name, "project": dt.project, "due_date": dt.due_date}  # Use id instead of usn
        context.append(dd)
    print(context)
    return render_template('todo.html', todo=context)

@app.route('/add-task')
def add_task():
    return render_template('add_task.html')

@app.route('/submit', methods=['POST'])
def create_user():
    name = request.form['name']
    project = request.form['project']
    due_date = request.form['due_date']
    print(f"name is: {name}, project is: {project}, and due_date is: {due_date}")
    new_task = Todo1(name=name, project=project, due_date=due_date)
    print("new_task: {}".format(new_task))
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('add_task'))

@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_user(id):
    task = Todo1.query.get(id)

    if not task:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred while deleting the data: {e}'}), 500

@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo1.query.get_or_404(id)

    if not task:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':
        task.name = request.form['name']
        task.project = request.form['project']
        task.due_date = request.form['due_date']

        try:
            db.session.commit()
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return "There was an issue while updating the record."

    return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
