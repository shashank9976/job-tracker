def create_company(client):
    return client.post("/companies", json={"name": "Contact Company", "tier": "B"}).json()["id"]


def contact_payload(company_id):
    return {"company_id": company_id, "first_name": "Ada", "last_name": "Lovelace", "status": "Not Started"}


def test_contact_create_list_get_update_delete(client):
    company_id = create_company(client)
    created = client.post("/contacts", json=contact_payload(company_id))
    assert created.status_code == 201
    contact_id = created.json()["id"]

    assert len(client.get("/contacts").json()) == 1
    assert client.get(f"/contacts/{contact_id}").json()["first_name"] == "Ada"

    updated = client.put(f"/contacts/{contact_id}", json={"status": "Emails Sent", "email": "ada@example.com"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "Emails Sent"

    patched = client.patch(f"/contacts/{contact_id}/status", json={"status": "Replied"})
    assert patched.status_code == 200
    assert patched.json()["status"] == "Replied"

    assert client.delete(f"/contacts/{contact_id}").status_code == 204
    assert client.get(f"/contacts/{contact_id}").status_code == 404


def test_contact_validation_failure(client):
    response = client.post("/contacts", json={"company_id": 1, "first_name": "Only"})
    assert response.status_code == 422
