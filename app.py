'''
Flask Application
'''
from flask import Flask, jsonify, request
from spellchecker import SpellChecker
from models import Experience, Education, Skill

# Initialize the spell checker
spell = SpellChecker()

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
                  "University of Technology",
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
        experience_data = request.get_json()
        # Validate the json data
        if not all(key in experience_data for key in ['title', 'company', 'start_date',
                                                      'end_date', 'description', 'logo']):
            return jsonify({"error": "Missing required fields"}), 400

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

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/experience/<int:index>', methods=['GET'])
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
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

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
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


def spell_check_text(text):
    """
    Checks and corrects spelling in a sentence.

    Parameters
    ----------
    text : str
        The input sentence to be checked.

    Returns
    -------
    dict or None
        A dictionary with 'before' and 'after' keys if corrections are found,
        otherwise None.
    """
    words = text.split()
    corrected = {}

    for word in words:
        if word in spell:
            continue
        correction = spell.correction(word)
        if correction and correction != word:
            # Match the original casing...
            if word.isupper():
                correction = correction.upper()
            elif word.istitle():
                correction = correction.title()
            elif word.islower():
                correction = correction.lower()
            corrected[word] = correction

    if corrected:
        corrected_text = ' '.join([
            corrected.get(w, w)
            for w in words
        ])
        return {
            "before": text,
            "after": corrected_text
        }
    return None


@app.route('/resume/spellcheck', methods=['GET'])
def spellcheck_resume_entries():
    """
    Performs spell check on Experience, Education, and Skill entries.

    Returns
    -------
    Response
        A JSON list of objects showing spelling corrections. Each object
        contains 'before' and 'after' fields representing the original and 
        corrected text respectively.
    """
    corrections = []

    for section in ['experience', 'education', 'skill']:
        for item in data[section]:
            item_dict = item.__dict__ if hasattr(item, '__dict__') else item
            for _, value in item_dict.items():
                if isinstance(value, str):
                    correction = spell_check_text(value)
                    if correction:
                        corrections.append(correction)

    return jsonify(corrections), 200
