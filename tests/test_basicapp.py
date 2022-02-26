from fixtures import client


def tests_home_url_status_is_200(client):
    response = client.get("/")

    assert response.status_code == 200
