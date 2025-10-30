from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    """Test that the root endpoint redirects to index.html"""
    response = client.get("/", follow_redirects=False)  # Don't follow the redirect
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    # Test structure of an activity
    first_activity = list(activities.values())[0]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity

def test_signup_for_activity(client: TestClient):
    """Test signing up for an activity"""
    # Get first activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Try signing up with a new email
    test_email = "test_student@mergington.edu"
    response = client.post(
        f"/activities/{activity_name}/signup",
        json={"email": test_email}
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert test_email in activities[activity_name]["participants"]

def test_duplicate_signup(client: TestClient):
    """Test that a student cannot sign up for the same activity twice"""
    # Get first activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    test_email = "duplicate_test@mergington.edu"
    
    # First signup should succeed
    response = client.post(
        f"/activities/{activity_name}/signup",
        json={"email": test_email}
    )
    assert response.status_code == 200
    
    # Second signup should fail
    response = client.post(
        f"/activities/{activity_name}/signup",
        json={"email": test_email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_nonexistent_activity(client: TestClient):
    """Test signing up for a non-existent activity"""
    response = client.post(
        "/activities/NonexistentActivity/signup",
        json={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_from_activity(client: TestClient):
    """Test unregistering from an activity"""
    # Get first activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    test_email = "unregister_test@mergington.edu"
    
    # First sign up for the activity
    response = client.post(
        f"/activities/{activity_name}/signup",
        json={"email": test_email}
    )
    assert response.status_code == 200
    
    # Then unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert test_email not in activities[activity_name]["participants"]

def test_unregister_not_registered(client: TestClient):
    """Test unregistering when not registered"""
    # Get first activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    test_email = "not_registered@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()

def test_unregister_nonexistent_activity(client: TestClient):
    """Test unregistering from a non-existent activity"""
    response = client.delete(
        "/activities/NonexistentActivity/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()