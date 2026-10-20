"""Experience, education, certifications and security endpoints."""

import pytest

pytestmark = pytest.mark.anyio


async def test_experience_returns_list(client):
    response = await client.get("/api/v1/experience")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # intentionally empty until real data is added


async def test_education(client):
    response = await client.get("/api/v1/education")
    assert response.status_code == 200
    entry = response.json()[0]
    assert set(entry) == {
        "degree", "field", "institution", "location", "start_date", "end_date", "description",
    }
    assert (entry["degree"], entry["field"], entry["institution"]) == (
        "B.Tech", "Information Technology", "SGSITS Indore",
    )


async def test_certifications_returns_list(client):
    response = await client.get("/api/v1/certifications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_security_overview(client):
    response = await client.get("/api/v1/security")
    assert response.status_code == 200
    body = response.json()
    assert [c["category"] for c in body["categories"]] == [
        "Web Security", "Network Security", "Linux", "API Security",
        "Reconnaissance", "Security Testing",
    ]
    assert {t["name"] for t in body["tools"]} == {
        "Nmap", "Burp Suite", "Wireshark", "Hydra", "Hashcat", "VirusTotal",
    }
    categories = {c["category"] for c in body["categories"]}
    assert all(t["category"] in categories for t in body["tools"])


async def test_security_has_no_numeric_ratings(client):
    body = (await client.get("/api/v1/security")).json()

    def numbers(node):
        if isinstance(node, bool):
            return []
        if isinstance(node, (int, float)):
            return [node]
        if isinstance(node, dict):
            return [n for v in node.values() for n in numbers(v)]
        if isinstance(node, list):
            return [n for v in node for n in numbers(v)]
        return []

    assert numbers(body) == []
