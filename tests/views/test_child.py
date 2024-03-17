"""Tests for Child views."""

from flask.testing import FlaskClient


def test_children_list(client: FlaskClient) -> None:
    response = client.get("/children")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Enzo" in data


def test_child_management(client: FlaskClient) -> None:
    create_child = client.post(
        "/child/create",
        follow_redirects=True,
        data={
            "first_name": "Théo",
            "family_name": "POUSSIN",
            "gender_iso": 1,
            "birthdate": "2024-01-10",
        },
    )
    print(create_child.headers)
    print(create_child.text)
    assert create_child.status_code == 200

    list_children = client.get("/children")
    assert list_children.status_code == 200
    assert "Théo" in list_children.data.decode()

    detail_child = client.get("/child/4")
    assert detail_child.status_code == 200
    assert "Théo" in detail_child.data.decode()

    delete_child = client.get("/child/4/delete", follow_redirects=True)
    assert delete_child.status_code == 200
    assert "Théo" not in delete_child.data.decode()
