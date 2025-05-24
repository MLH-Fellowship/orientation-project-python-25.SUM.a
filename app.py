'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import validate_data
import os
import openai

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
                  "Learned various concepts in CS.",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}

openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_API_KEY_HERE") # Replace with your actual key or ensure OPENAI_API_KEY is set

def get_openai_suggestions(description: str, section_name: str) -> list[str]:
    """
    Gets suggestions from OpenAI for a given description.
    """
    try:
        prompt = f"Rewrite this {section_name} description to be more impactful and concise. Provide 3 variations:\\n\\n{description}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that helps improve resume descriptions."},
                {"role": "user", "content": prompt}
            ],
            n=3, # Ask for 3 suggestions
            stop=None,
            temperature=0.7,
        )
        suggestions = [choice.message['content'].strip() for choice in response.choices]
        return suggestions
    except Exception as e:
        print(f"Error getting OpenAI suggestions: {e}")
        return []

@app.route('/test')
def hello_world():
    """
    Returns a test message.

    Returns
    -------
    Response
        JSON response with a greeting message.
    """
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
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
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/experience/<int:index>', methods=['GET', 'PUT'])
def get_experience_by_index(index):
    """
    Retrieves or updates an experience entry by index.

    Parameters
    ----------
    index : int
        The index of the experience entry.

    Returns
    -------
    Response
        JSON of the experience entry if found (GET), success message (PUT),
        otherwise 404 or 400 error.
    """
    if request.method == 'GET':
        try:
            experience_item = data['experience'][index]
            return jsonify(experience_item)
        except IndexError:
            return jsonify({"error": "Experience not found"}), 404

    if request.method == 'PUT':
        try:
            experience_data = request.get_json()
            is_valid, error_message = validate_data('experience', experience_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            # Create a new Experience object with updated data to ensure structure
            updated_experience = Experience(
                experience_data.get('title', data['experience'][index].title),
                experience_data.get('company', data['experience'][index].company),
                experience_data.get('start_date', data['experience'][index].start_date),
                experience_data.get('end_date', data['experience'][index].end_date),
                experience_data.get('description', data['experience'][index].description),
                experience_data.get('logo', data['experience'][index].logo)
            )
            data['experience'][index] = updated_experience
            return jsonify({"message": "Experience updated successfully"}), 200
        except IndexError:
            return jsonify({"error": "Experience not found"}), 404
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/experience/<int:index>/suggest-description', methods=['POST'])
def suggest_experience_description(index):
    """
    Suggests improvements for an experience description using OpenAI.
    """
    try:
        experience_item = data['experience'][index]
        current_description = experience_item.description # Assuming Experience object has a description attribute
        
        # Optionally, allow passing description in request body to override
        request_data = request.get_json()
        if request_data and 'description' in request_data:
            current_description = request_data['description']

        if not current_description:
            return jsonify({"error": "Description is empty"}), 400

        suggestions = get_openai_suggestions(current_description, "professional experience")
        
        if not suggestions:
            return jsonify({"error": "Could not generate suggestions"}), 500
            
        return jsonify({"suggestions": suggestions}), 200
    except IndexError:
        return jsonify({"error": "Experience not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


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
            
            new_education = Education(
                education_data['course'],
                education_data['school'],
                education_data['start_date'],
                education_data['end_date'],
                education_data['grade'],
                education_data.get('description', ""), # Add description, default to empty string
                education_data['logo']
            )
            data['education'].append(new_education)
            return jsonify({"id": len(data['education']) - 1}), 201
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({})

@app.route('/resume/education/<int:index>', methods=['GET', 'PUT', 'DELETE'])
def education_by_index(index):
    '''
    Handles education requests by index
    This function handles HTTP requests:
    - GET: Retrieves a specific education by index
    - PUT: Updates a specific education by index
    - DELETE: Deletes a specific education by index
    '''
    if request.method == 'GET':
        try:
            education_item = data['education'][index]
            return jsonify(education_item)
        except IndexError:
            return jsonify({"error": "Education not found"}), 404
    if request.method == 'PUT':
        try:
            education_data = request.get_json()
            is_valid, error_message = validate_data('education', education_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            # Create a new Education object with updated data
            updated_education = Education(
                education_data.get('course', data['education'][index].course),
                education_data.get('school', data['education'][index].school),
                education_data.get('start_date', data['education'][index].start_date),
                education_data.get('end_date', data['education'][index].end_date),
                education_data.get('grade', data['education'][index].grade),
                education_data.get('description', data['education'][index].description),
                education_data.get('logo', data['education'][index].logo)
            )
            data['education'][index] = updated_education
            return jsonify({"message": "Education updated successfully"}), 200
        except IndexError:
            return jsonify({"error": "Education not found"}), 404
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400
    if request.method == 'DELETE':
        if 0 <= index < len(data["education"]):
            data["education"].pop(index)
            return jsonify({"message": "Education has been deleted"}), 200
        return jsonify({"error": "400 Bad Request"}), 400
    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/education/<int:index>/suggest-description', methods=['POST'])
def suggest_education_description(index):
    """
    Suggests improvements for an education description using OpenAI.
    """
    try:
        education_item = data['education'][index]
        current_description = education_item.description # Assuming Education object has a description attribute

        # Optionally, allow passing description in request body to override
        request_data = request.get_json()
        if request_data and 'description' in request_data:
            current_description = request_data['description']

        if not current_description:
            return jsonify({"error": "Description is empty"}), 400

        suggestions = get_openai_suggestions(current_description, "education")

        if not suggestions:
            return jsonify({"error": "Could not generate suggestions"}), 500

        return jsonify({"suggestions": suggestions}), 200
    except IndexError:
        return jsonify({"error": "Education not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    """
    Handles skill data requests.

    GET: Returns all stored skill entries.
    POST: Adds a new skill entry (to be implemented).

    Returns
    -------
    Response
        JSON of skill data (or empty placeholder) on GET.
        Returns 405 if method is not allowed.
    """
    if request.method == 'GET':
        return jsonify(data['skill']), 200

    if request.method == 'POST':
        try:
            skill_data = request.get_json()
            is_valid, error_message = validate_data('skill', skill_data)
            if not is_valid:
                return jsonify({"error": error_message}), 400
            # pylint: disable=fixme
            # TODO: Create new Skill object with skill_data
            # TODO: Append new skill to data['skill']
            # TODO: Return jsonify({"id": len(data['skill']) - 1}), 201
            return jsonify({}), 201
        except (TypeError, ValueError, KeyError):
            return jsonify({"error": "Invalid data format"}), 400

    return jsonify({})
