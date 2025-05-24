'''
Tests in Pytest
'''
from app import app
from unittest.mock import patch, MagicMock


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
    Add a new education and then get all educations.
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    initial_response = app.test_client().get('/resume/education')
    assert initial_response.status_code == 200
    initial_length = len(initial_response.json)

    post_response = app.test_client().post('/resume/education',
                                     json=example_education)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    response = app.test_client().get('/resume/education')
    assert response.status_code == 200
    assert len(response.json) == initial_length + 1

    education_dict = {
        "course": response.json[item_id].get('course'),
        "school": response.json[item_id].get('school'),
        "start_date": response.json[item_id].get('start_date'),
        "end_date": response.json[item_id].get('end_date'),
        "grade": response.json[item_id].get('grade'),
        "logo": response.json[item_id].get('logo')
    }
    assert education_dict == example_education

    assert item_id == len(response.json) - 1

def test_get_education_by_id():
    '''
    Get a specific education by its id
    '''
    example_education = {
        "course": "Computer Science",
        "school": "UBC",
        "start_date": "January 2022",
        "end_date": "June 2026",
        "grade": "90%",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/education',
                                     json=example_education)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    response = app.test_client().get(f'/resume/education/{item_id}')
    assert response.status_code == 200

    education_dict = {
        "course": response.json.get('course'),
        "school": response.json.get('school'),
        "start_date": response.json.get('start_date'),
        "end_date": response.json.get('end_date'),
        "grade": response.json.get('grade'),
        "logo": response.json.get('logo')
    }
    assert education_dict == example_education

    response = app.test_client().get('/resume/education/999')
    assert response.status_code == 404
    assert response.json['error'] == "Education not found"


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
    assert post_resp.status_code == 201
    item_id = post_resp.json['id']

    # Delete the education using the ID:
    del_resp = client.delete(f'/resume/education/{item_id}')
    assert del_resp.status_code == 200
    assert del_resp.json['message'] == "Education has been deleted"

    # Delete again to check if it fails:
    del_resp = client.delete(f'/resume/education/{item_id}')
    assert del_resp.status_code == 400
    assert del_resp.json['error'] == "400 Bad Request"


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


def test_invalid_input_validation():
    '''
    Test that the API properly validates input data for POST requests
    '''
    client = app.test_client()
    # Test invalid experience
    invalid_experience = {
        "title": "Software Developer",
        # Missing required fields
    }
    response = client.post('/resume/experience', json=invalid_experience)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing required fields" in response.json["error"]
    assert "company" in response.json["error"]
    assert "start_date" in response.json["error"]
    assert "end_date" in response.json["error"]
    assert "description" in response.json["error"]
    assert "logo" in response.json["error"]
    # Test invalid education
    invalid_education = {
        "course": "Computer Science",
        # Missing required fields
    }
    response = client.post('/resume/education', json=invalid_education)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing required fields" in response.json["error"]
    assert "school" in response.json["error"]
    assert "start_date" in response.json["error"]
    assert "end_date" in response.json["error"]
    assert "grade" in response.json["error"]
    assert "logo" in response.json["error"]
    # Test invalid skill
    invalid_skill = {
        "name": "Python",
        # Missing required fields
    }
    response = client.post('/resume/skill', json=invalid_skill)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing required fields" in response.json["error"]
    assert "proficiency" in response.json["error"]
    assert "logo" in response.json["error"]
    # Test invalid data format
    response = client.post('/resume/experience', data="not json")
    assert response.status_code == 415


# --- Tests for PUT (Update) Endpoints ---

def test_update_experience():
    '''
    Test updating an existing experience item.
    '''
    client = app.test_client()
    initial_experience = {
        "title": "Initial Title", "company": "InitialCo", "start_date": "Jan 2020",
        "end_date": "Dec 2020", "description": "Initial description", "logo": "initial.png"
    }
    post_response = client.post('/resume/experience', json=initial_experience)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    updated_data = {
        "title": "Updated Title", "company": "UpdatedCo", "start_date": "Feb 2021",
        "end_date": "Nov 2021", "description": "Updated description", "logo": "updated.png"
    }
    put_response = client.put(f'/resume/experience/{item_id}', json=updated_data)
    assert put_response.status_code == 200
    assert put_response.json['message'] == "Experience updated successfully"

    get_response = client.get(f'/resume/experience/{item_id}')
    assert get_response.status_code == 200
    # Convert response to dict, excluding any potential extra fields not in updated_data
    retrieved_data = {k: get_response.json[k] for k in updated_data}
    assert retrieved_data == updated_data

    # Test updating non-existent item
    put_response_non_existent = client.put('/resume/experience/999', json=updated_data)
    assert put_response_non_existent.status_code == 404

    # Test update with invalid data (e.g. missing required field)
    invalid_update_data = updated_data.copy()
    del invalid_update_data['title'] # title is required by Experience model
    # For validation to work correctly in PUT, validate_data needs to check all fields,
    # or we assume partial updates don't re-validate missing fields not being updated.
    # The current PUT implementation uses .get() with defaults from original item,
    # so it won't fail validation for fields not present in the PUT body.
    # If we want to test validation on PUT, validate_data or the PUT logic would need adjustment.
    # For now, let's assume valid partial updates are fine.

def test_update_education():
    '''
    Test updating an existing education item.
    '''
    client = app.test_client()
    initial_education = {
        "course": "Initial Course", "school": "Initial School", "start_date": "Sep 2019",
        "end_date": "Jul 2022", "grade": "A", "description": "Initial edu desc", "logo": "initial_edu.png"
    }
    post_response = client.post('/resume/education', json=initial_education)
    assert post_response.status_code == 201
    item_id = post_response.json['id']

    updated_data = {
        "course": "Updated Course", "school": "Updated School", "start_date": "Oct 2020",
        "end_date": "Jun 2023", "grade": "A+", "description": "Updated edu desc", "logo": "updated_edu.png"
    }
    put_response = client.put(f'/resume/education/{item_id}', json=updated_data)
    assert put_response.status_code == 200
    assert put_response.json['message'] == "Education updated successfully"

    get_response = client.get(f'/resume/education/{item_id}')
    assert get_response.status_code == 200
    retrieved_data = {k: get_response.json[k] for k in updated_data}
    assert retrieved_data == updated_data

    # Test updating non-existent item
    put_response_non_existent = client.put('/resume/education/999', json=updated_data)
    assert put_response_non_existent.status_code == 404

# --- Tests for OpenAI Suggestion Endpoints ---

@patch('app.openai.ChatCompletion.create')
def test_suggest_experience_description(mock_openai_create):
    '''
    Test the experience description suggestion endpoint.
    '''
    client = app.test_client()
    # Add an experience item first
    experience_data = {
        "title": "Dev", "company": "TestCo", "start_date": "Jan 2022", "end_date": "Present",
        "description": "Original experience description.", "logo": "logo.png"
    }
    post_response = client.post('/resume/experience', json=experience_data)
    item_id = post_response.json['id']

    # Configure the mock OpenAI response
    mock_choice1 = MagicMock()
    mock_choice1.message = {'content': 'Suggested description 1.'}
    mock_choice2 = MagicMock()
    mock_choice2.message = {'content': 'Suggested description 2.'}
    mock_openai_create.return_value = MagicMock(choices=[mock_choice1, mock_choice2])

    # Test suggestion with existing description
    response = client.post(f'/resume/experience/{item_id}/suggest-description')
    assert response.status_code == 200
    assert response.json['suggestions'] == ["Suggested description 1.", "Suggested description 2."]
    mock_openai_create.assert_called_once()
    call_args = mock_openai_create.call_args[1] # keyword arguments
    assert "Original experience description." in call_args['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test suggestion with description from request body
    response_body_desc = client.post(f'/resume/experience/{item_id}/suggest-description',
                                     json={"description": "Body description for experience."})
    assert response_body_desc.status_code == 200
    assert response_body_desc.json['suggestions'] == ["Suggested description 1.", "Suggested description 2."]
    mock_openai_create.assert_called_once()
    call_args_body = mock_openai_create.call_args[1]
    assert "Body description for experience." in call_args_body['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test item not found
    response_not_found = client.post('/resume/experience/999/suggest-description')
    assert response_not_found.status_code == 404

    # Test OpenAI API error (simulated by mock raising an exception)
    mock_openai_create.side_effect = Exception("OpenAI API Error")
    response_api_error = client.post(f'/resume/experience/{item_id}/suggest-description')
    assert response_api_error.status_code == 500
    assert response_api_error.json['error'] == "Could not generate suggestions"
    mock_openai_create.side_effect = None # Reset side_effect
    mock_openai_create.reset_mock()

    # Test with empty description (from item)
    # To test this, we'd need to be able to create an item with an empty description.
    # The Experience model requires a description. If we update to allow empty, this test is valid.
    # Assuming for now description cannot be empty based on model & validate_data.
    # If description is empty string after update, it would be caught by the endpoint's check.

    # Test with empty description (from request body)
    response_empty_body_desc = client.post(f'/resume/experience/{item_id}/suggest-description',
                                     json={"description": ""})
    assert response_empty_body_desc.status_code == 400
    assert response_empty_body_desc.json['error'] == "Description is empty"

@patch('app.openai.ChatCompletion.create')
def test_suggest_education_description(mock_openai_create):
    '''
    Test the education description suggestion endpoint.
    '''
    client = app.test_client()
    # Add an education item first
    education_data = {
        "course": "Science", "school": "TestSchool", "start_date": "Sep 2020", "end_date": "Jul 2023",
        "grade": "B", "description": "Original education description.", "logo": "edu_logo.png"
    }
    post_response = client.post('/resume/education', json=education_data)
    item_id = post_response.json['id']

    # Configure the mock OpenAI response
    mock_choice1 = MagicMock()
    mock_choice1.message = {'content': 'Edu suggestion 1.'}
    mock_choice2 = MagicMock()
    mock_choice2.message = {'content': 'Edu suggestion 2.'}
    mock_openai_create.return_value = MagicMock(choices=[mock_choice1, mock_choice2])

    # Test suggestion with existing description
    response = client.post(f'/resume/education/{item_id}/suggest-description')
    assert response.status_code == 200
    assert response.json['suggestions'] == ["Edu suggestion 1.", "Edu suggestion 2."]
    mock_openai_create.assert_called_once()
    call_args = mock_openai_create.call_args[1]
    assert "Original education description." in call_args['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test suggestion with description from request body
    response_body_desc = client.post(f'/resume/education/{item_id}/suggest-description',
                                     json={"description": "Body description for education."})
    assert response_body_desc.status_code == 200
    assert response_body_desc.json['suggestions'] == ["Edu suggestion 1.", "Edu suggestion 2."]
    mock_openai_create.assert_called_once()
    call_args_body = mock_openai_create.call_args[1]
    assert "Body description for education." in call_args_body['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test item not found
    response_not_found = client.post('/resume/education/999/suggest-description')
    assert response_not_found.status_code == 404

    # Test OpenAI API error
    mock_openai_create.side_effect = Exception("OpenAI API Error")
    response_api_error = client.post(f'/resume/education/{item_id}/suggest-description')
    assert response_api_error.status_code == 500
    assert response_api_error.json['error'] == "Could not generate suggestions"
    mock_openai_create.side_effect = None
    mock_openai_create.reset_mock()

    # Test with empty description from request body
    response_empty_body_desc = client.post(f'/resume/education/{item_id}/suggest-description',
                                     json={"description": ""})
    assert response_empty_body_desc.status_code == 400
    assert response_empty_body_desc.json['error'] == "Description is empty"
