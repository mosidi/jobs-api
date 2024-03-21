def test_create_user(client):
    """
    Test the creation of a user by sending a POST request to the "/users/register" endpoint with the provided data.

    Args:
        client (TestClient): The test client used to send the request.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200 or if the email or is_active fields in the response JSON do not match the expected values.
    """
    data = {
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
    }
    response = client.post("/users/register", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"]
