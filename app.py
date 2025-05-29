"""
Flask Application
"""

from dataclasses import fields
from flask import Flask, jsonify, request
from spellchecker import SpellChecker
from models import Experience, Education, Skill

# Initialize the spell checker
spell = SpellChecker()

app = Flask(__name__)

data = {
    "experience": [
        Experience(
            "Software Developer",
            "A Cool Company",
            "October 2022",
            "Present",
            "Writing Python Code",
            "example-logo.png",
        )
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [Skill("Python", "1-2 Years", "example-logo.png")],
}


@app.route("/test")
def hello_world():
    """
    Returns a test message.

    Returns
    -------
    Response
        JSON response with a greeting message.
    """
    return jsonify({"message": "Hello, World!"})


@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handles experience data requests.

    GET: Returns all stored experience entries.
    POST: Adds a new experience entry.

    Returns
    -------
    Response
        JSON list of experience entries (on GET) or a new entry ID (on POST).
        Returns 400 if required fields are missing in POST.
        Returns 405 if method is not allowed.
    """
    if request.method == "GET":
        return jsonify(data["experience"]), 200

    if request.method == "POST":
        try:
            experience_data = request.get_json()
            is_valid, error_message = validate_data("experience", experience_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            new_experience = Experience(
                experience_data["title"],
                experience_data["company"],
                experience_data["start_date"],
                experience_data["end_date"],
                experience_data["description"],
                experience_data["logo"],
            )
            data["experience"].append(new_experience)
            return jsonify({"id": len(data["experience"]) - 1}), 201
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({"error": "Method not allowed"}), 405


@app.route("/resume/experience/<int:index>", methods=["GET"])
def get_experience_by_index(index):
    """
    Retrieves an experience entry by index.

    Parameters
    ----------
    index : int
        The index of the experience entry to retrieve.

    Returns
    -------
    Response
        JSON of the experience entry if found, otherwise 404 error.
    """
    try:
        experience_item = data["experience"][index]
        return jsonify(experience_item)
    except IndexError:
        return jsonify({"error": "Experience not found"}), 404


@app.route("/resume/experience/<int:item_id>", methods=["PUT"])
def update_experience(item_id):
    """
    Update an experience by index.

    Parameters
    ----------
    item_id : int
        The index of the experience to update.

    Returns
    -------
    Response
        JSON message indicating success or error.
        Returns 404 if experience not found
        Returns 400 if request is invalid.
    """
    content = request.json
    if not content:
        return jsonify({"error": "Invalid request"}), 400

    if 0 <= item_id < len(data["experience"]):
        try:
            valid_keys = {f.name for f in fields(Experience)}
            filtered_content = {k: v for k, v in content.items() if k in valid_keys}
            data["experience"][item_id] = Experience(**filtered_content)
            return jsonify({"message": "Experience updated successfully"}), 200
        except TypeError as e:
            return jsonify({"error": f"Missing or invalid fields: {str(e)}"}), 400

    return jsonify({"error": "Experience not found"}), 404


@app.route("/resume/education", methods=["GET", "POST"])
def education():
    """
    Handles education requests
    """
    if request.method == "GET":
        return jsonify(data["education"]), 200

    if request.method == "POST":
        try:
            education_data = request.get_json()
            is_valid, error_message = validate_data("education", education_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400
            # pylint: disable=fixme
            # TODO: Create new Education object with education_data
            # TODO: Append new education to data['education']
            # TODO: Return jsonify({"id": len(data['education']) - 1}), 201
            return jsonify({}), 201
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({})


@app.route("/resume/education/<int:index>", methods=["GET", "DELETE"])
def education_by_index(index):
    """
    Handles education requests by index
    This function handles two types of HTTP requests:
    - GET: Retrieves a specific education by index
    - DELETE: Deletes a specific education by index
    """
    if request.method == "GET":
        try:
            education_item = data["education"][index]
            return jsonify(education_item)
        except IndexError:
            return jsonify({"error": "Education not found"}), 404
    if request.method == "DELETE":
        if 0 <= index < len(data["education"]):
            data["education"].pop(index)
            return jsonify({"message": "Education has been deleted"}), 200
        return jsonify({"error": "400 Bad Request"}), 400
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/resume/education/<int:item_id>", methods=["PUT"])
def update_education(item_id):
    """
    Update an education by index.

    Parameters
    ----------
    item_id : int
        The index of the education to update.

    Returns
    -------
    Response
        JSON message indicating success or error.
        Returns 404 if education not found.
        Returns 400 if request is invalid.
    """
    content = request.json
    if not content:
        return jsonify({"error": "Invalid request"}), 400

    if 0 <= item_id < len(data["education"]):
        try:
            valid_keys = {f.name for f in fields(Education)}
            filtered_content = {k: v for k, v in content.items() if k in valid_keys}
            data["education"][item_id] = Education(**filtered_content)
            return jsonify({"message": "Education updated successfully"}), 200
        except TypeError as e:
            return jsonify({"error": f"Missing or invalid fields: {str(e)}"}), 400

    return jsonify({"error": "Education not found"}), 404


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})
