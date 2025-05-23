'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    # First get initial experiences
    initial_response = app.test_client().get('/resume/experience')
    assert initial_response.status_code == 200
    initial_length = len(initial_response.json)

    # Add new experience
    post_response = app.test_client().post('/resume/experience',
                                     json=example_experience)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    # Get updated experiences list
    response = app.test_client().get('/resume/experience')
    assert response.status_code == 200
    assert len(response.json) == initial_length + 1

    # Convert response data to dict for comparison
    experience_dict = {
        "title": response.json[item_id].get('title'),
        "company": response.json[item_id].get('company'),
        "start_date": response.json[item_id].get('start_date'),
        "end_date": response.json[item_id].get('end_date'),
        "description": response.json[item_id].get('description'),
        "logo": response.json[item_id].get('logo')
    }
    assert experience_dict == example_experience

    # Test that index matches position in list
    assert item_id == len(response.json) - 1


def test_get_experience_by_id():
    '''
    Get a specific experience by its id
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company", 
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    # First add an experience
    post_response = app.test_client().post('/resume/experience',
                                     json=example_experience)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    # Then retrieve it by id
    response = app.test_client().get(f'/resume/experience/{item_id}')
    assert response.status_code == 200

    # Convert response data to dict for comparison
    experience_dict = {
        "title": response.json.get('title'),
        "company": response.json.get('company'),
        "start_date": response.json.get('start_date'),
        "end_date": response.json.get('end_date'),
        "description": response.json.get('description'),
        "logo": response.json.get('logo')
    }
    assert experience_dict == example_experience

    # Test invalid index
    response = app.test_client().get('/resume/experience/999')
    assert response.status_code == 404
    assert response.json['error'] == "Experience not found"

def test_education():
    '''
    Test the /resume/education POST and GET endpoints.

    - Ensure an empty payload returns a 400 error.
    - Ensure missing required fields return a 400 error.
    - Successfully add a valid education entry.
    - Confirm the entry is correctly returned via GET.
    '''
    empty_education = {}
    missing_education = {
        "course": "Engineering",
        "school": "NYU",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    client = app.test_client()

    # Test empty payload:
    response = client.post('/resume/education', json=empty_education)
    assert response.status_code == 400
    assert response.json['error'] == "No data provided"

    # Test missing field:
    response = client.post('/resume/education', json=missing_education)
    assert response.status_code == 400
    assert response.json['error'] == "Missing required fields"

    # Test valid education:
    response = client.post('/resume/education', json=example_education)
    assert response.status_code == 201
    item_id = response.json['id']
    assert isinstance(item_id, int)
    assert item_id == 1

    # Test retrieval:
    # TODO: The GET endpoint needs to be implemented in `app.py` for this to pass. # pylint: disable=fixme
    response = client.get('/resume/education')
    assert response.status_code == 200
    assert response.json[item_id] == example_education

def test_delete_education():
    '''
    Add and delete an education entry by index.

    Check that the entry is deleted successfully and the response is correct.
    '''
    example_education = {
        "course": "Computer Science",
        "school": "UBC",
        "start_date": "January 2022",
        "end_date": "June 2026",
        "grade": "90%",
        "logo": "example-logo.png"
    }

    client = app.test_client()

    # Add new education:
    # TODO: Implement the '/resume/education' POST route in `app.py` before running this test. # pylint: disable=fixme
    post_resp = client.post('/resume/education', json=example_education)
    assert post_resp.status_code == 200
    item_id = post_resp.json['id']

    # Delete the education using the ID:
    del_resp = client.delete(f'/resume/education/{item_id}')
    assert del_resp.status_code == 200
    assert del_resp.json['message'] == "Education has been deleted"

    # Delete again to check if it fails:
    del_resp = client.delete(f'/resume/education/{item_id}')
    assert del_resp.status_code == 404
    assert del_resp.json['error'] == "Index out of range"


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill
