"""
Tests in Pytest
"""

from app import app
from unittest.mock import patch, MagicMock


def test_client():
    """
    Makes a request and checks the message received is the same
    """
    response = app.test_client().get("/test")
    assert response.status_code == 200
    assert response.json["message"] == "Hello, World!"
def test_experience():
    """
    Add a new experience and then get all experiences.

    Check that it returns the new experience in that list
    """
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": 
"example-logo.png",
    }

    # First get initial experiences
    initial_response = app.test_client().get("/resume/experience")
    assert initial_response.status_code == 200
    initial_length = len(initial_response.json)

    # Add new experience
    post_response = app.test_client().post(
        "/resume/experience", json=example_experience
    )
    assert post_response.status_code == 201
    item_id = post_response.json["id"]

    # Get updated experiences list
    response = app.test_client().get("/resume/experience")
    assert response.status_code == 200
    assert len(response.json) == initial_length + 
1

    # Convert response data to dict for comparison
    experience_dict = {
        "title": response.json[item_id].get("title"),
        "company": response.json[item_id].get("company"),
        "start_date": response.json[item_id].get("start_date"),
        "end_date": response.json[item_id].get("end_date"),
        "description": response.json[item_id].get("description"),
        "logo": response.json[item_id].get("logo"),
    }
    assert experience_dict == example_experience

    # Test that index matches position in list
    assert item_id == 
len(response.json) - 1


def test_get_experience_by_id():
    """
    Get a specific experience by its id
    """
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png",
    }

    # First add an experience
 
   post_response = app.test_client().post(
        "/resume/experience", json=example_experience
    )
    assert post_response.status_code == 201
    item_id = post_response.json["id"]

    # Then retrieve it by id
    response = app.test_client().get(f"/resume/experience/{item_id}")
    assert response.status_code == 200

    # Convert response data to dict for comparison
    experience_dict = {
        "title": response.json.get("title"),
        "company": response.json.get("company"),
        "start_date": response.json.get("start_date"),
   
     "end_date": response.json.get("end_date"),
        "description": response.json.get("description"),
        "logo": response.json.get("logo"),
    }
    assert experience_dict == example_experience

    # Test invalid index
    response = app.test_client().get("/resume/experience/999")
    assert response.status_code == 404
    assert response.json["error"] == "Experience not found"


def test_update_experience():
    """
    Update an experience and check that it correctly updates.
"""
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png",
    }

    item_id = (
        app.test_client().post("/resume/experience", json=example_experience).json["id"]
    )
    updated_data = {**example_experience, "title": "Senior Software Dev"}
   
 response = app.test_client().put(f"/resume/experience/{item_id}", json=updated_data)

    assert response.status_code == 200
    response_data = response.json
    assert response_data["message"] == "Experience updated successfully"
    get_response = app.test_client().get("/resume/experience")
    updated_experience = get_response.json[item_id]

    assert updated_experience["title"] == updated_data["title"]
    assert updated_experience["company"] == updated_data["company"]
    assert updated_experience["start_date"] == updated_data["start_date"]
    assert updated_experience["end_date"] == updated_data["end_date"]
    assert updated_experience["description"] == updated_data["description"]
    assert updated_experience["logo"] == updated_data["logo"]


def test_update_experience_with_unknown_field():
    """
    Update an experience with a field not part of the Experience 
model.
    This should still return 200, but the unknown field should not be saved.
"""
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png",
    }

    updated_experience = {
        **example_experience,
        "title": "Updated Title",
        
"new_field": "This should not be saved",
    }

    item_id = (
        app.test_client().post("/resume/experience", json=example_experience).json["id"]
    )
    response = app.test_client().put(
        f"/resume/experience/{item_id}", json=updated_experience
    )
    assert response.status_code == 200
    get_response = app.test_client().get("/resume/experience")
    saved_data = get_response.json[item_id]
    assert "new_field" not in saved_data
    assert saved_data["title"] == "Updated Title"


def test_update_experience_invalid_id():
    """
    Update an experience with an invalid id and check 
that it returns a 404
    """
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png",
    }

    item_id = (
        app.test_client().post("/resume/experience", json=example_experience).json["id"]
    )
    updated_experience 
= {**example_experience, "company": "New Company"}
    response = app.test_client().put(
        f"/resume/experience/{item_id + 1}", json=updated_experience
    )
    assert response.status_code == 404
    response_data = response.json
    assert response_data["error"] == "Experience not found"


def test_update_experience_with_missing_fields():
    """
    Try updating an experience with missing required fields.
Should return 400 Bad Request.
    """
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png",
    }

    invalid_update = {
        "company": "New Company",
        "start_date": "June 2025",
 
       "end_date": "Present",
        "description": "Updated Description",
        "logo": "new-logo.png",
    }

    item_id = (
        app.test_client().post("/resume/experience", json=example_experience).json["id"]
    )
    response = app.test_client().put(
        f"/resume/experience/{item_id}", json=invalid_update
    )
    assert response.status_code == 400
    assert "error" in response.json

def test_delete_experience(): # This function appears twice in the original, keeping the first instance.
    """
    add an experience entry
    delete 
that experience entry by index.
    Check that it is deleted successfully with correct response.
"""
    example_experience = {
        "title": "Backend Engineer",
        "company": "Google",
        "start_date": "March 2023",
        "end_date": "Present",
        "description": "Working on scalable systems",
        "logo": "example-logo.png",
    }

    post_response = app.test_client().post("/resume/experience", json=example_experience)
    assert post_response.status_code == 201
    item_id = post_response.json["id"]
    delete_response = app.test_client().delete(f"/resume/experience/{item_id}")
    assert 
delete_response.status_code == 200
    assert delete_response.json["message"] == "Experience has been deleted"
    delete_response = app.test_client().delete(f"/resume/experience/{item_id}")
    assert delete_response.status_code == 400 # Attempting to delete again
    assert delete_response.json["error"] == "Invalid request" # Or "Experience not found" depending on implementation


def test_education():
    """
    Add a new education and then get all educations.
Check that it returns the new education in that list
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png",
    }

    initial_response = app.test_client().get("/resume/education")
    assert initial_response.status_code == 200
    initial_length = len(initial_response.json)

  
  post_response = app.test_client().post("/resume/education", json=example_education)
    assert post_response.status_code == 201
    item_id = post_response.json["id"]

    response = app.test_client().get("/resume/education")
    assert response.status_code == 200
    assert len(response.json) == initial_length + 1

    education_dict = {
        "course": response.json[item_id].get("course"),
        "school": response.json[item_id].get("school"),
        "start_date": response.json[item_id].get("start_date"),
        "end_date": response.json[item_id].get("end_date"),
        "grade": response.json[item_id].get("grade"),
        "logo": 
response.json[item_id].get("logo"),
    }
    assert education_dict == example_education

    assert item_id == len(response.json) - 1


def test_get_education_by_id():
    """
    Get a specific education by its id
    """
    example_education = {
        "course": "Computer Science",
        "school": "UBC",
        "start_date": "January 2022",
        "end_date": "June 2026",
        "grade": "90%",
       
 "logo": "example-logo.png",
    }

    post_response = app.test_client().post("/resume/education", json=example_education)
    assert post_response.status_code == 201
    item_id = post_response.json["id"]

    response = app.test_client().get(f"/resume/education/{item_id}")
    assert response.status_code == 200

    education_dict = {
        "course": response.json.get("course"),
        "school": response.json.get("school"),
        "start_date": response.json.get("start_date"),
        "end_date": response.json.get("end_date"),
        "grade": response.json.get("grade"),
        "logo": response.json.get("logo"),
 
   }
    assert education_dict == example_education

    response = app.test_client().get("/resume/education/999")
    assert response.status_code == 404
    assert response.json["error"] == "Education not found"


def test_update_education(): # This function is defined twice, once before the conflict, once inside. Using the one from edit-existing-skill.
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
    # Ensuring all keys from updated_data are present and match in the response
    retrieved_data = {k: get_response.json.get(k) for k in updated_data}
    assert retrieved_data == updated_data

    # Test updating non-existent item
    put_response_non_existent = client.put('/resume/education/999', json=updated_data)
    assert put_response_non_existent.status_code == 404


def test_update_education_with_unknown_field():
    """
    Update an education with a field not part of the Education model.
This should still return 200, but the unknown field should not be saved.
"""
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png",
    }

    updated_education = {
        **example_education,
        "course": "Health Sciences",
        "new_field": "This 
should not be saved",
    }

    item_id = (
        app.test_client().post("/resume/education", json=example_education).json["id"]
    )
    response = app.test_client().put(
        f"/resume/education/{item_id}", json=updated_education
    )

    assert response.status_code == 200
    get_response = app.test_client().get(f"/resume/education/{item_id}") # Use f-string for ID
    saved_data = get_response.json
    assert "new_field" not in saved_data
    assert saved_data["course"] == "Health Sciences"


def test_update_education_invalid_id():
    """
    Update an education with an invalid id and check that it 
returns a 404
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png",
    }

    # Add an item to ensure there's something, though we'll use an invalid ID for the PUT
    app.test_client().post("/resume/education", json=example_education).json["id"]
    
    updated_education = {**example_education, "course": "Changed 
Course"}
    # Use a deliberately invalid ID (e.g., a high number unlikely to exist)
    response = app.test_client().put(
        f"/resume/education/99999", json=updated_education # Using a fixed large number
    )

    assert response.status_code == 404
    response_data = response.json
    assert response_data["error"] == "Education not found"


def test_update_education_with_missing_fields():
    """
    Try updating an education with missing required fields.
Should return 400 Bad Request.
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png",
    }

    invalid_update = { # Missing "school"
        "course": "Physics",
        "start_date": "January 2023",
    
    "end_date": "May 2024",
        "grade": "90%",
        "logo": "new-logo.png",
    }

    item_id = (
        app.test_client().post("/resume/education", json=example_education).json["id"]
    )
    response = app.test_client().put(
        f"/resume/education/{item_id}", json=invalid_update
    )
    assert response.status_code == 400 # Assuming PUT validates all required fields
    assert "error" in response.json


def test_delete_education():
    """
    Add and delete an education entry by index.
Check that the entry is deleted successfully and the response is correct.
"""
    example_education = {
        "course": "Computer Science",
        "school": "UBC",
        "start_date": "January 2022",
        "end_date": "June 2026",
        "grade": "90%",
        "logo": "example-logo.png",
    }

    client = app.test_client()

    # Add new education:
    post_resp = client.post('/resume/education', json=example_education)
    assert post_resp.status_code == 201
    item_id = 
post_resp.json['id']

    # Delete the education using the ID:
    del_resp = client.delete(f"/resume/education/{item_id}")
    assert del_resp.status_code == 200
    assert del_resp.json["message"] == "Education has been deleted"

    # Delete again to check if it fails:
    del_resp_again = client.delete(f"/resume/education/{item_id}") # Renamed variable
    assert del_resp_again.status_code == 404 # Should be 404 Not Found if already deleted
    assert "Education not found" in del_resp_again.json["error"] # Adjusted expected error message


def test_skill():
    """
    Add a new skill and then get all skills.
Check that it returns the new skill in that list
    """
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png",
    }
    
    client = app.test_client() # Define client
    post_response = client.post("/resume/skill", json=example_skill) # Use client
    assert post_response.status_code == 201 # Expect 201 for creation
    item_id = post_response.json["id"]

    response = client.get("/resume/skill") # Use client
    # Check if the skill is in the list of skills (assuming GET /resume/skill returns a list)
    # This check might need adjustment based on the actual structure of response.json
    found_skill = False
    if isinstance(response.json, list): # If it's a list of skills
        for skill in response.json:
            if skill.get("id") == item_id: # Assuming items have 'id'
                # Compare relevant fields, excluding 'id' if it's not in example_skill
                skill_to_compare = {k: skill[k] for k in example_skill}
                assert skill_to_compare == example_skill
                found_skill = True
                break
        assert found_skill, "Posted skill not found in the list of skills"
    elif isinstance(response.json, dict): # If it's a dict keyed by id
         assert response.json[str(item_id)] == example_skill # Assuming ID is string key
    else:
        assert False, "Unexpected response format for GET /resume/skill"


def test_skill_missing_fields():
    """
    Add a new skill with missing field and check that it returns an error
    """
   
 example_skill = {"name": "JavaScript", "logo": "example-logo.png"} # Missing proficiency
    response = app.test_client().post("/resume/skill", json=example_skill)

    assert response.status_code == 400
    assert "Missing required fields" in response.json["error"] # More specific check
    assert "proficiency" in response.json["error"] # Check if "proficiency" is mentioned as missing


def test_skill_id_return():
    """
    Make sure the id of newly added skill is returned.
"""

    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "eniola.png",
    }
    response = app.test_client().post("/resume/skill", json=example_skill)
    assert response.status_code == 201
    assert "id" in response.json


def test_invalid_input_validation():
    """
    Test that the API properly validates input data for POST requests
    """
    client = app.test_client()
    # Test invalid experience
    invalid_experience 
= {
        "title": "Software Developer",
        # Missing required fields
    }
    response = client.post("/resume/experience", json=invalid_experience)
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
    response = client.post("/resume/education", json=invalid_education)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing required fields" in response.json["error"]
    assert "school" in response.json["error"]
    assert "start_date" in response.json["error"]
    assert "end_date" in response.json["error"]
    assert "grade" in response.json["error"]
    assert "logo" in response.json["error"]
    # Test 
invalid skill
    invalid_skill = {
        "name": "Python",
        # Missing required fields
    }
    response = client.post("/resume/skill", json=invalid_skill)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing required fields" in response.json["error"]
    assert "proficiency" in response.json["error"]
    assert "logo" in response.json["error"]
    # Test invalid data format
    response = client.post("/resume/experience", data="not json")
    assert response.status_code == 415


# --- Tests for PUT (Update) Endpoints --- [cite: 45]

def test_update_experience(): # This is distinct from the earlier test_update_experience by its content
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
        "end_date": "Nov 2021", "description": "Updated 
description", "logo": "updated.png"
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
    put_response_non_existent = client.put('/resume/experience/999', json=updated_data) # Use a non-existent ID
    assert put_response_non_existent.status_code == 404

  
  # Test update with invalid data (e.g. missing required field)
    invalid_update_data = updated_data.copy()
    del invalid_update_data['title'] # title is required by Experience model
    put_invalid_response = client.put(f'/resume/experience/{item_id}', json=invalid_update_data) # Use existing item_id
    assert put_invalid_response.status_code == 400 # Expecting validation to fail
    assert "Missing required fields" in put_invalid_response.json['error'] # Assuming error message format
    assert "title" in put_invalid_response.json['error']

# test_update_education is already defined above from[cite: 52, 53, 54], this block is a duplicate from the merge.
# The earlier version [cite: 27, 28] and the merge conflict version [cite: 52, 53, 54] are similar.
# I'll use the one from [cite: 52, 53, 54] as it's part of the `edit-existing-skill` branch's new additions.
# This was handled by replacing the original `test_update_education` with the one from `edit-existing-skill`.

# --- Tests for OpenAI Suggestion Endpoints --- [cite: 54]

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
    assert post_response.status_code == 201 # Ensure item is created
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
    assert "Original experience description."
in call_args['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test suggestion with description from request body
    response_body_desc = client.post(f'/resume/experience/{item_id}/suggest-description',
                                     json={"description": "Body description for experience."})
    assert response_body_desc.status_code == 200
    assert response_body_desc.json['suggestions'] == ["Suggested description 1.", "Suggested description 2."]
    mock_openai_create.assert_called_once()
    call_args_body = mock_openai_create.call_args[1]
    assert "Body description for 
experience." in call_args_body['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test item not found
    response_not_found = client.post('/resume/experience/999/suggest-description') # Use a non-existent ID
    assert response_not_found.status_code == 404

    # Test OpenAI API error (simulated by mock raising an exception)
    mock_openai_create.side_effect = Exception("OpenAI API Error")
    response_api_error = client.post(f'/resume/experience/{item_id}/suggest-description')
    assert response_api_error.status_code == 500
    assert response_api_error.json['error'] == "Could not generate suggestions"
    mock_openai_create.side_effect = None # Reset side_effect
    mock_openai_create.reset_mock()

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
        "grade": "B", "description": "Original education description.", "logo": "edu_logo.png" # Added description for consistency
    }
    post_response = client.post('/resume/education', json=education_data)
    assert post_response.status_code == 201 # Ensure item is created
    item_id = post_response.json['id']

    # Configure the mock OpenAI response
    mock_choice1 = MagicMock()
    mock_choice1.message = {'content': 'Edu suggestion 1.'}
    mock_choice2 = 
MagicMock()
    mock_choice2.message = {'content': 'Edu suggestion 2.'}
    mock_openai_create.return_value = MagicMock(choices=[mock_choice1, mock_choice2])

    # Test suggestion with existing description
    response = client.post(f'/resume/education/{item_id}/suggest-description')
    assert response.status_code == 200
    assert response.json['suggestions'] == ["Edu suggestion 1.", "Edu suggestion 2."]
    mock_openai_create.assert_called_once()
    call_args = mock_openai_create.call_args[1]
    assert "Original education description."
in call_args['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test suggestion with description from request body
    response_body_desc = client.post(f'/resume/education/{item_id}/suggest-description',
                                     json={"description": "Body description for education."})
    assert response_body_desc.status_code == 200
    assert response_body_desc.json['suggestions'] == ["Edu suggestion 1.", "Edu suggestion 2."]
    mock_openai_create.assert_called_once()
    call_args_body = mock_openai_create.call_args[1]
    assert "Body description for 
education." in call_args_body['messages'][1]['content']
    mock_openai_create.reset_mock()

    # Test item not found
    response_not_found = client.post('/resume/education/999/suggest-description') # Use a non-existent ID
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

def test_update_skill():
    """
    Add a skill, then update it and check if the changes are reflected.
"""
    client = app.test_client() # Define client
    # Add a skill
    example_skill_to_add = {
        "name": "InitialPyTestSkill",
        "proficiency": "Beginner",
    
    "logo": "initial_logo.png"
    }
    post_response = client.post('/resume/skill', json=example_skill_to_add)
    assert post_response.status_code == 201 # Expect 201 for creation
    item_id_to_update = post_response.json['id']

    # Data for updating the skill
    skill_update_payload = {
        "name": "Updated PyTestSkill",

        "proficiency": "Intermediate",
        "logo": "updated_logo.png"
    }

    # Perform the PUT request
    put_response = client.put(f'/resume/skill/{item_id_to_update}', 
                                         json=skill_update_payload)
    assert put_response.status_code == 200
    assert put_response.json['message'] == "Skill updated successfully"

# Verify the skill was updated by fetching it directly if possible, or checking the list
    # Assuming GET /resume/skill/{id} exists, or adapting to GET /resume/skill list
    get_response = client.get(f'/resume/skill/{item_id_to_update}') # Assumes GET by ID
    if get_response.status_code == 404 and get_response.json.get("error") == "Method Not Allowed": # Fallback if GET /resume/skill/{id} not implemented
        get_all_skills_response = client.get('/resume/skill')
        assert get_all_skills_response.status_code == 200
        updated_skill_data = None
        for skill in get_all_skills_response.json:
            if skill.get("id") == item_id_to_update:
                updated_skill_data = skill
                break
        assert updated_skill_data is not None, "Updated skill not found in the list"
    else: # Assumes GET /resume/skill/{id} is implemented
        assert get_response.status_code == 200
        updated_skill_data = get_response.json
    
    assert updated_skill_data['name'] == skill_update_payload['name']
    assert updated_skill_data['proficiency'] == skill_update_payload['proficiency']
    assert updated_skill_data['logo'] == skill_update_payload['logo']

    # Test updating a non-existent skill
    non_existent_id = item_id_to_update + 999 # An ID that surely doesn't exist
    put_response_not_found = client.put(f'/resume/skill/{non_existent_id}', 
                                      
           json=skill_update_payload)
    assert put_response_not_found.status_code == 404
    assert put_response_not_found.json['error'] == "Skill not found"

    # Test updating with invalid data (e.g., missing 'name')
    invalid_payload = {
        "proficiency": "Expert",
        "logo": "invalid.png"
    }
    
    put_response_invalid_data = client.put(f'/resume/skill/{item_id_to_update}', # Use existing valid ID
         
                                             json=invalid_payload)
    assert put_response_invalid_data.status_code == 400
    assert "Missing required fields" in put_response_invalid_data.json['error'] # Check error message
    assert "name" in put_response_invalid_data.json['error'] # Specifically "name"

# --- Tests from main branch ---

def test_delete_skill():
    """
    Add and delete a skill by index (actually ID)

    Check that the skill is deleted and the response is correct
    """

    example_skill 
= {
        "name": "JavaToDelete", # Using a unique name for this test
        "proficiency": "1-5 years",
        "logo": "example-logo.png",
    }

    client = app.test_client()

    # Add new skill
    post_response = client.post("/resume/skill", json=example_skill)
    assert post_response.status_code == 201 # Assuming 201 for successful creation
    item_id = post_response.json["id"] # Assuming "id" is returned, not "index"

    # Delete skill
    delete_response = client.delete(f"/resume/skill/{item_id}")
    assert delete_response.status_code == 200
    # Check message, or if the item is truly gone from a subsequent GET
    assert delete_response.json["message"] == "Skill has been deleted" # Assuming this message

    # Optionally, verify it's gone
    get_response = client.get(f"/resume/skill/{item_id}") # Assuming GET by ID exists
    if not (get_response.status_code == 404 and get_response.json.get("error") == "Method Not Allowed"): # Skip if GET by ID not implemented
        assert get_response.status_code == 404 # Should be Not Found


def test_get_skill_by_id(): # Renamed from test_get_skill_by_index for clarity if using ID
    """
 Add a new skill then get specific skill by ID
    """
    example_skill = {
        "name": "JavaToGet", # Unique name
        "proficiency": "1-5 years",
        "logo": "example-logo.png",
    }

    client = app.test_client()

    # Add skill
    post_response = client.post("/resume/skill", json=example_skill) # Endpoint was "resume/skill"
    assert post_response.status_code == 201 # Assuming 201 for successful creation
    item_id = post_response.json["id"] # Assuming "id"

    # Retrieve skill by ID
    response = client.get(f'/resume/skill/{item_id}') # Changed to GET from POST, and used f-string
  
  assert response.status_code == 200
    # Compare the retrieved skill with the example_skill (excluding id if not in example_skill)
    retrieved_skill = {k: response.json[k] for k in example_skill}
    assert retrieved_skill == example_skill