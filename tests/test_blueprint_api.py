from fixtures import client, item


def tests_if_api_sends_200(client):
    response = client.get("/api/v1/")

    assert response.status_code == 200


def tests_if_api_root_returns_list(client):
    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert type(response.get_json()) is list


def tests_if_api_posts_new_item(client, item):
    response = client.post(
        "/api/v1/",
        json=item,
    )

    assert response.status_code == 201
    assert "id" in response.get_json()
    assert item["titulo"] == response.get_json()["titulo"]
    assert item["descricao"] == response.get_json()["descricao"]


def tests_if_api_refuses_to_add_duplicated_item(client, item):
    first_add = client.post(
        "/api/v1/",
        json=item,
    )

    response = client.post(
        "/api/v1/",
        json=item,
    )

    assert response.status_code == 406


def tests_if_api_returns_specific_existing_item(client, item):
    first_add = client.post(
        "/api/v1/",
        json=item,
    )

    response = client.get(f"/api/v1/{first_add.get_json()['id']}")

    assert response.status_code == 200
    assert response.get_json()["titulo"] == item["titulo"]
    assert response.get_json()["descricao"] == item["descricao"]


def tests_if_api_fails_on_get_non_existing(client):
    response = client.get("/api/v1/1")

    assert response.status_code == 404


def tests_if_api_updates_on_non_existing_fails(client, item):
    item["id"] = 1
    response = client.put("/api/v1/", json=item)

    assert response.status_code == 403


def tests_if_api_updates_on_duplicate_fails(client, item):
    first_add = client.post(
        "/api/v1/",
        json=item,
    )

    item["titulo"] = "Feijoada"
    second_add = client.post(
        "/api/v1/",
        json=item,
    )

    update = first_add.get_json()
    update["titulo"] = "Feijoada"

    response = client.put("/api/v1/", json=update)

    assert response.status_code == 406


def tests_if_api_updates_existing_item(client, item):
    first_add = client.post(
        "/api/v1/",
        json=item,
    )

    update = first_add.get_json()

    update["titulo"] = "Feijoada"

    response = client.put("/api/v1/", json=update)

    assert response.status_code == 201
    assert response.get_json()["titulo"] == update["titulo"]


def tests_if_api_deletes_non_existing_item_fail(client, item):
    item["id"] = 2

    response = client.delete("/api/v1/", json=item)

    assert response.status_code == 404


def tests_if_api_deletes_existing_item_fail(client, item):
    first_add = client.post(
        "/api/v1/",
        json=item,
    )

    response = client.delete("/api/v1/", json=first_add.get_json())

    assert response.status_code == 201
