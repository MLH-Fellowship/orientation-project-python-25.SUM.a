"""
Tests in Pytest
"""

from app import app


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
        "logo": "example-logo.png",
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
    assert len(response.json) == initial_length + 1

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
    assert item_id == len(response.json) - 1


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
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience', json=example_experience).json['id']
    updated_data = {**example_experience, "title": "Senior Software Dev"}
    response = app.test_client().put(f'/resume/experience/{item_id}', json=updated_data)

    assert response.status_code == 200
    response_data = response.json
    assert response_data['message'] == "Experience updated successfully"
    get_response = app.test_client().get('/resume/experience')
    updated_experience = get_response.json[item_id]

    assert updated_experience["title"] == updated_data['title']
    assert updated_experience["company"] == updated_data['company']
    assert updated_experience["start_date"] == updated_data['start_date']
    assert updated_experience["end_date"] == updated_data['end_date']
    assert updated_experience["description"] == updated_data['description']
    assert updated_experience["logo"] == updated_data['logo']

def test_update_experience_with_unknown_field():
    """
    Update an experience with a field not part of the Experience model.
    This should still return 200, but the unknown field should not be saved.
    """
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png"
    }

    updated_experience = {
        **example_experience,
        "title": "Updated Title",
        "new_field": "This should not be saved"
    }

    item_id = app.test_client().post('/resume/experience', json=example_experience).json['id']
    response = app.test_client().put(f'/resume/experience/{item_id}', json=updated_experience)
    assert response.status_code == 200
    get_response = app.test_client().get('/resume/experience')
    saved_data = get_response.json[item_id]
    assert "new_field" not in saved_data
    assert saved_data["title"] == "Updated Title"

def test_update_experience_invalid_id():
    """
    Update an experience with an invalid id and check that it returns a 404
    """
    example_experience = {
        "title": "Software Developer",
        "company": "G-research",
        "start_date": "May 2025",
        "end_date": "Present",
        "description": "Writing C-sharp Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience', json=example_experience).json['id']
    updated_experience = {**example_experience, 'company': 'New Company'}
    response = app.test_client().put(f'/resume/experience/{item_id + 1}', json=updated_experience)
    assert response.status_code == 404
    response_data = response.json
    assert response_data['error'] == "Experience not found"


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
        "logo": "example-logo.png"
    }

    invalid_update = {
        "company": "New Company",
        "start_date": "June 2025",
        "end_date": "Present",
        "description": "Updated Description",
        "logo": "new-logo.png"
    }

    item_id = app.test_client().post('/resume/experience', json=example_experience).json['id']
    response = app.test_client().put(f'/resume/experience/{item_id}', json=invalid_update)
    assert response.status_code == 400
    assert "error" in response.json


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
        "logo": response.json[item_id].get("logo"),
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

def test_update_education():
    """
    Update an education and check that it correctly updates.
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/education', json=example_education).json['id']
    updated_data = {**example_education, "course": "Computer Science"}
    response = app.test_client().put(f'/resume/education/{item_id}', json=updated_data)

    assert response.status_code == 200
    response_data = response.json
    assert response_data['message'] == "Education updated successfully"

    get_response = app.test_client().get('/resume/education')
    updated_education = get_response.json[item_id]

    assert updated_education["course"] == updated_data['course']
    assert updated_education["school"] == updated_data['school']
    assert updated_education["start_date"] == updated_data['start_date']
    assert updated_education["end_date"] == updated_data['end_date']
    assert updated_education["grade"] == updated_data['grade']
    assert updated_education["logo"] == updated_data['logo']


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
        "logo": "example-logo.png"
    }

    updated_education = {
        **example_education,
        "course": "Health Sciences",
        "new_field": "This should not be saved"
    }

    item_id = app.test_client().post('/resume/education', json=example_education).json['id']
    response = app.test_client().put(f'/resume/education/{item_id}', json=updated_education)

    assert response.status_code == 200
    get_response = app.test_client().get('/resume/education')
    saved_data = get_response.json[item_id]
    assert "new_field" not in saved_data
    assert saved_data["course"] == "Health Sciences"


def test_update_education_invalid_id():
    """
    Update an education with an invalid id and check that it returns a 404
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/education', json=example_education).json['id']
    updated_education = {**example_education, 'course': 'Changed Course'}
    response = app.test_client().put(f'/resume/education/{item_id + 1}', json=updated_education)

    assert response.status_code == 404
    response_data = response.json
    assert response_data['error'] == "Education not found"

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
        "logo": "example-logo.png"
    }

    invalid_update = {
        "course": "Physics",
        "start_date": "January 2023",
        "end_date": "May 2024",
        "grade": "90%",
        "logo": "new-logo.png"
    }

    item_id = app.test_client().post('/resume/education', json=example_education).json['id']
    response = app.test_client().put(f'/resume/education/{item_id}', json=invalid_update)
    assert response.status_code == 400
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
    # TODO: Implement the '/resume/education' POST route in `app.py` before running this test. # pylint: disable=fixme
    post_resp = client.post("/resume/education", json=example_education)
    assert post_resp.status_code == 200
    item_id = post_resp.json["id"]

    # Delete the education using the ID:
    del_resp = client.delete(f"/resume/education/{item_id}")
    assert del_resp.status_code == 200
    assert del_resp.json["message"] == "Education has been deleted"

    # Delete again to check if it fails:
    del_resp = client.delete(f"/resume/education/{item_id}")
    assert del_resp.status_code == 400
    assert del_resp.json["error"] == "400 Bad Request"


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

    item_id = app.test_client().post("/resume/skill", json=example_skill).json["id"]

    response = app.test_client().get("/resume/skill")
    assert response.json[item_id] == example_skill


def test_skill_missing_fields():
    """
    Add a new skill with missing field and check that it returns an error
    """
    example_skill = {"name": "JavaScript", "logo": "example-logo.png"}
    response = app.test_client().post("/resume/skill", json=example_skill)

    assert response.status_code == 400
    assert response.json["error"] == "Missing required fields"


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
    invalid_experience = {
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
    # Test invalid skill
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
