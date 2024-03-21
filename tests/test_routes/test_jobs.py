from fastapi import status


def test_read_main(client):
    """
    Function to test the read operation in the main endpoint.
    Takes a client as parameter.
    No return value.
    """
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_job(client, normal_user_token_headers):

    data = {
        "job_title": "SDE super",
        "job_company": "doogle",
        "job_company_url": "www.doogle.com",
        "job_location": "USA,NY",
        "job_description": "python",
        "job_date_posted": "2022-03-20",
    }
    response = client.post(
        "/jobs/create/", json=data, headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["job_company"] == "doogle"
    assert response.json()["job_description"] == "python"


def test_read_job(client, normal_user_token_headers):
    """
    Function for testing the read job functionality.

    Parameters:
    - client: the HTTP client object
    - normal_user_token_headers: the headers containing the normal user token

    """
    data = {
        "job_title": "SDE super",
        "job_company": "doogle",
        "job_company_url": "www.doogle.com",
        "job_location": "USA,NY",
        "job_description": "python",
        "job_date_posted": "2022-03-20",
    }
    response = client.post(
        "/jobs/create/", json=data, headers=normal_user_token_headers
    )
    response = client.get("/jobs/get/1/")
    assert response.status_code == 200
    assert response.json()["job_title"] == "SDE super"


def test_read_all_jobs(client, normal_user_token_headers):
    """
    Test the functionality of reading all jobs from the API.

    Args:
        client (TestClient): The test client for making HTTP requests.
        normal_user_token_headers (dict): The headers containing the authentication token for a normal user.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200 or if the response JSON does not contain the expected data.

    """
    data = {
        "job_title": "SDE super",
        "job_company": "doogle",
        "job_company_url": "www.doogle.com",
        "job_location": "USA,NY",
        "job_description": "python",
        "job_date_posted": "2022-03-20",
    }
    client.post("/jobs/create/", json=data, headers=normal_user_token_headers)
    client.post("/jobs/create/", json=data)

    response = client.get("/jobs/all/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_a_job(client, normal_user_token_headers):
    """
    Test the update of a job by making a PUT request to the '/jobs/update/1' endpoint.

    Parameters:
        client (TestClient): The test client used to make HTTP requests.
        normal_user_token_headers (dict): The headers containing the authentication token for a normal user.

    Returns:
        None

    Raises:
        AssertionError: If the response JSON does not contain the expected value for the 'detail' key.
    """
    data = {
        "job_title": "SDE super",
        "job_company": "doogle",
        "job_company_url": "www.doogle.com",
        "job_location": "USA,NY",
        "job_description": "python",
        "job_date_posted": "2022-03-20",
    }
    client.post("/jobs/create/", json=data, headers=normal_user_token_headers)
    data["job_title"] = "test new title"
    response = client.put(
        "/jobs/update/1", json=data, headers=normal_user_token_headers
    )
    assert response.json()["detail"] == "Successfully updated data."


def test_delete_a_job(client, normal_user_token_headers):
    """
    A function to test deleting a job using client and normal_user_token_headers.
    """
    data = {
        "job_title": "SDE super",
        "job_company": "doogle",
        "job_company_url": "www.doogle.com",
        "job_location": "USA,NY",
        "job_description": "python",
        "job_date_posted": "2022-03-20",
    }
    response = client.post(
        "/jobs/create/", json=data, headers=normal_user_token_headers
    )
    response = client.delete("/jobs/delete/1", headers=normal_user_token_headers)

    response = client.get("/jobs/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
