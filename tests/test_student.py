def get_auth_token(client, username="student_tester", password="pass123"):
    # Register the user
    client.post("/auth/register", json={"username": username, "password": password})
    # Login to get token
    response = client.post(
        "/auth/login", 
        json={"username": username, "password": password}
    )
    return response.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_get_students_without_token(client):
    response = client.get("/students/")
    # Expect unauthorized (401 or 403 depending on your app)
    assert response.status_code in [401, 403]


def test_get_students_with_token(client):
    token = get_auth_token(client, username="getter_user")
    response = client.get("/students/", headers=auth_header(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_student(client):
    token = get_auth_token(client, username="creator_user")
    response = client.post(
        "/students/",
        json={
            "name": "Ravi Kumar",
            "age": 20,
            "email": "ravi@test.com",
            "city": "Kuppam"
        },
        headers=auth_header(token)
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ravi Kumar"
    assert data["email"] == "ravi@test.com"

    assert "id" in data    
