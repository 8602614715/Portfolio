import pytest

pytestmark = pytest.mark.anyio

PUBLIC_FIELDS = {
    "name", "headline", "secondary_title", "bio", "location",
    "email", "github_url", "linkedin_url", "resume_url",
}


async def test_get_profile(client):
    response = await client.get("/api/v1/profile")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == PUBLIC_FIELDS  # no id / timestamps / private fields
    assert body["name"] == "Satyam Prajapati"
    assert body["headline"]


async def test_profile_missing_returns_404(client):
    from app.db.database import get_session
    from app.main import app

    class EmptyResult:
        def scalar_one_or_none(self):
            return None

    class EmptySession:
        async def execute(self, *_args, **_kwargs):
            return EmptyResult()

    async def override():
        yield EmptySession()

    app.dependency_overrides[get_session] = override
    response = await client.get("/api/v1/profile")
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": {"code": "PROFILE_NOT_FOUND", "message": "Profile not found"},
    }
