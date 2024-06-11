from flask import Flask, render_template, request, jsonify
#from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models_crud import initialize_database, create_task, update_task
# from auth import auth_bp  # Import the Blueprint
from config import Config, DevelopmentConfig, ProductionConfig
from sqlalchemy import text, exc
from flask_cors import CORS
import os
 
from extensions import db
 
app = Flask(__name__)
 
CORS(app)
 
config_class='DevelopmentConfig'
config_class = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')
app.config.from_object(f'config.{config_class}')
 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'mysql+pymysql://user:password@dbMySQL:3306/mydatabase'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kimhoe.gcit:P06coqOWytAT@ep-little-hall-a1ykg9bf.ap-southeast-1.aws.neon.tech/usmdb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
 
# Pushing the application context correctly
with app.app_context():
    initialize_database()

# check taskId exist or not
def taskid_exist(taskId):
    result = db.session.execute(text("SELECT 1 FROM Task WHERE taskId = :taskId"), {'taskId': taskId}).fetchone()
    if not result:
        return jsonify({'message': 'Task not found'}), 404
    return None

# check data missing or not
def data_missing(data, required_data):
    missing_data = []
    for field in required_data:
        if field not in data:
            missing_data.append(field)

    if missing_data:
        return jsonify({
            'message': 'Task creation failed',
            'details': f"Missing fields: {', '.join(missing_data)}"
        }), 400
    return None
 
@app.route("/")
def hello():
    return render_template("index.html")
    # return "Hello, World!"

# create newe task
@app.route("/tasks", methods=['POST'])
def create_new_task ():
    data = request.get_json()

    # If the request body is missing name or description or points, return 400
    valid_error = data_missing(data, ['name', 'desc', 'points'])
    if valid_error:
        return valid_error
    
    # import data
    name = data.get('name')
    desc = data.get('desc')
    points = data.get('points')
    image_url = data.get('image_url')

    try:
        task = create_task(name, desc, points, image_url)
        return jsonify({"message": "Task created successfully", "task": task}), 201
    
    except Exception as e:
        return jsonify({"message": "Task creation failed", "details": str(e)}), 500

# update task by id
@app.route('/tasks/<int:taskId>', methods=['PUT'])
def update_task_by_id(taskId):
    # check taskId
    task_error = taskid_exist(taskId)
    if task_error:
        return task_error
    
    data = request.get_json()
    # check data missing
    valid_error = data_missing(data, ['name', 'desc', 'points'])
    if valid_error:
        return valid_error
    
    name = data.get('name')
    desc = data.get('desc')
    points = data.get('points')
    image_url = data.get('image_url')

    try:
        task = update_task(taskId, name, desc, points, image_url)
        if 'error' in task:
            return jsonify(task), 400
        else:
            return jsonify(task), 200
    except Exception as e:
        return jsonify({'message': 'Task update failed', 'details': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
