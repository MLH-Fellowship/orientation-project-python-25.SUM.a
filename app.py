'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

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
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})
        

    return jsonify({})


@app.route('/resume/skill/<int:index>', methods=['GET'])
def get_skill_by_index(index):
    """
    Get a specific skill by index
    """
    try:
        skill_index = data['skill'][index]
        return jsonify(skill_index), 200
    except IndexError:
        return jsonify({"error": "Skill not found"}), 404
    

@app.route('/resume/skill/<int:index>', methods=['DELETE'])
def delete_skill(index):
    if 0 <= index < len(data["skill"]):
        data["skill"].pop(index)
        return jsonify({"message": "Successfully deleted skill"}), 200
    
    return jsonify({"error": "Skill not found"}), 404