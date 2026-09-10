from datetime import date, timedelta


def test_stats_summary_by_tier_and_reminders(client):
    company = client.post("/companies", json={"name": "Stats Co", "tier": "A", "priority": "High", "followup_threshold_days": 8}).json()
    company_id = company["id"]
    client.post("/contacts", json={"company_id": company_id, "first_name": "Old", "last_name": "Contact", "date_sent": (date.today() - timedelta(days=7)).isoformat(), "status": "Emails Sent"})
    client.post("/contacts", json={"company_id": company_id, "first_name": "Replied", "last_name": "Contact", "date_sent": (date.today() - timedelta(days=7)).isoformat(), "status": "Replied", "replied": True})

    summary = client.get("/stats/summary")
    assert summary.status_code == 200
    assert summary.json() == {"total_companies": 1, "total_contacts": 2, "total_emails_sent": 2, "total_replies": 1, "reply_rate": 50.0}

    by_tier = client.get("/stats/by-tier")
    assert by_tier.status_code == 200
    assert by_tier.json() == [{"tier": "A", "company_count": 1, "emails_sent": 2}]

    reminders = client.get("/reminders")
    assert reminders.status_code == 200
    assert reminders.json() == []
    assert len(client.get("/reminders?threshold=7").json()) == 1
    assert client.get("/reminders?threshold=9").json() == []
