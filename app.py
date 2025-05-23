'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import validate_data

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handles experience requests
    This function handles two types of HTTP requests:
    - GET: Retrieves all experience data.
    - POST: Adds new experience data.
    '''
    if request.method == 'GET':
        return jsonify(data['experience']), 200

    if request.method == 'POST':
        try:
            experience_data = request.get_json()
            is_valid, error_message = validate_data('experience', experience_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            new_experience = Experience(
                experience_data['title'],
                experience_data['company'],
                experience_data['start_date'],
                experience_data['end_date'],
                experience_data['description'],
                experience_data['logo']
            )
            data['experience'].append(new_experience)
            return jsonify({"id": len(data['experience']) - 1}), 201
        except Exception:
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/experience/<int:index>', methods=['GET'])
def get_experience_by_index(index):
    '''
    Get a specific experience by index
    '''
    try:
        experience_item = data['experience'][index]
        return jsonify(experience_item)
    except IndexError:
        return jsonify({"error": "Experience not found"}), 404


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify(data['education']), 200

    if request.method == 'POST':
        try:
            education_data = request.get_json()
            is_valid, error_message = validate_data('education', education_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400
            return jsonify({}), 201
        except Exception:
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({})


@app.route('/resume/education/<int:index>', methods=['DELETE'])
def delete_education(index):
    """
    Deletes an education entry at the specified index.

    Parameters
    ----------
    index : int
        The index of the education entry to delete.

    Returns
    -------
    Response
        JSON response indicating success (with `deleted: True`) or
        failure (with an error message and 404 status code).
    """
    if 0 <= index < len( data[ "education" ] ):
        data[ "education" ].pop( index )
        return jsonify( { "message": "Education has been deleted" } ), 200
    return jsonify( { "error": "Index out of range" } ), 404


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify(data['skill']), 200

    if request.method == 'POST':
        try:
            skill_data = request.get_json()
            is_valid, error_message = validate_data('skill', skill_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400
            return jsonify({}), 201
        except Exception:
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({})
