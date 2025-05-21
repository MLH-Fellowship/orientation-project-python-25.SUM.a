"""
Flask Application
"""

from flask import Flask, jsonify, request
from models import Experience, Education, Skill

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
        Education(
            "Computer Science",
            "University of Tech",
            "September 2019",
            "July 2022",
            "80%",
            "example-logo.png",
        )
    ],
    "skill": [Skill("Python", "1-2 Years", "example-logo.png")],
}


@app.route("/test")
def hello_world():
    """
    Returns a JSON test message
    """
    return jsonify({"message": "Hello, World!"})


@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handle experience requests
    """
    if request.method == "GET":
        return jsonify()

    if request.method == "POST":
        return jsonify({})

    return jsonify({})


@app.route("/resume/education", methods=["GET", "POST"])
def education():
    """
    Handles education requests
    """
    if request.method == "GET":
        return jsonify({})

    if request.method == "POST":
        return jsonify({})

    return jsonify({})


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    """
    Handles Skill requests
    """
    if request.method == "GET":
        return jsonify(data["skill"])

    if request.method == "POST":
        if "name" not in request.json or not request.json["name"]:
            return jsonify({"error": "Name is required"}), 400
        if "proficiency" not in request.json or not request.json["proficiency"]:
            return jsonify({"error": "Proficiency is required"}), 400
        if "logo" not in request.json or not request.json["logo"]:
            return jsonify({"error": "Logo is required"}), 400
        data["skill"].append(
            Skill(
                request.json["name"], request.json["proficiency"], request.json["logo"]
            )
        )
        return jsonify({"id": len(data["skill"]) - 1}), 201

    return jsonify({})
