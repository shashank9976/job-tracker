def company_payload():
    return {
        "name": "Test Company",
        "tier": "A",
        "hq_location": "Bengaluru",
        "priority": "High",
        "status": "Not Started",
    }


def test_company_create_list_get_update_delete(client):
    created = client.post("/companies", json=company_payload())
    assert created.status_code == 201
    company_id = created.json()["id"]

    listed = client.get("/companies")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/companies/{company_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Test Company"

    updated = client.put(f"/companies/{company_id}", json={"status": "Researching", "people_found": 2})
    assert updated.status_code == 200
    assert updated.json()["status"] == "Researching"
    assert updated.json()["people_found"] == 2

    deleted = client.delete(f"/companies/{company_id}")
    assert deleted.status_code == 204
    assert client.get(f"/companies/{company_id}").status_code == 404


def test_company_validation_failure(client):
    response = client.post("/companies", json={"tier": "A"})
    assert response.status_code == 422
