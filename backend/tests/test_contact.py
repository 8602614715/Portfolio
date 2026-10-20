import pytest

pytestmark = pytest.mark.anyio

URL = "/api/v1/contact"
VALID = {"name": "Ada Lovelace", "email": "ada@example.com", "message": "Hello Satyam, great portfolio!"}


async def test_valid_message_is_stored(client, db_query):
    response = await client.post(URL, json=VALID)
    assert response.status_code == 201
    assert response.json() == {
        "success": True,
        "message": "Thanks for reaching out! Your message has been received.",
    }
    rows = await db_query("SELECT name, email, message FROM contact_messages")
    assert [tuple(r) for r in rows] == [(VALID["name"], VALID["email"], VALID["message"])]


async def test_response_never_echoes_input_or_ids(client):
    body = (await client.post(URL, json=VALID)).json()
    assert set(body) == {"success", "message"}


async def test_input_is_normalised(client, db_query):
    payload = {"name": "  Ada   Lovelace ", "email": "ADA@Example.COM", "message": "  hello there!  "}
    assert (await client.post(URL, json=payload)).status_code == 201
    rows = await db_query("SELECT name, email, message FROM contact_messages")
    assert [tuple(r) for r in rows] == [("Ada Lovelace", "ada@example.com", "hello there!")]


@pytest.mark.parametrize("name", ["सत्यम प्रजापति", "O'Brien-Smith", "José Ñúñez", "J. R. R. Tolkien"])
async def test_international_names_accepted(client, name):
    assert (await client.post(URL, json={**VALID, "name": name})).status_code == 201


@pytest.mark.parametrize("email", ["nope", "a@", "@example.com", "a b@example.com", "", "a@example"])
async def test_invalid_email(client, email):
    response = await client.post(URL, json={**VALID, "email": email})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"][0]["field"] == "email"


@pytest.mark.parametrize("message", ["", "   ", "\n\n\t", "hi"])
async def test_empty_or_too_short_message(client, message):
    response = await client.post(URL, json={**VALID, "message": message})
    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["field"] == "message"


async def test_oversized_message(client, db_query):
    response = await client.post(URL, json={**VALID, "message": "a" * 2001})
    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["field"] == "message"
    assert await db_query("SELECT 1 FROM contact_messages") == []


async def test_message_at_max_length_accepted(client):
    assert (await client.post(URL, json={**VALID, "message": "a" * 2000})).status_code == 201


@pytest.mark.parametrize(
    "name", ["", "A", "x" * 101, "<script>alert(1)</script>", "Bob123", "a--b", "-Ada", "Ada\u0000"]
)
async def test_invalid_name(client, name):
    response = await client.post(URL, json={**VALID, "name": name})
    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["field"] == "name"


async def test_control_characters_rejected_but_newlines_allowed(client):
    bad = await client.post(URL, json={**VALID, "message": "hello\u0000world, null byte"})
    assert bad.status_code == 422
    good = await client.post(URL, json={**VALID, "message": "line one\nline two\n\tindented"})
    assert good.status_code == 201


async def test_html_in_message_is_stored_as_inert_text(client, db_query):
    message = "<b>hello</b> <script>alert(1)</script>"
    assert (await client.post(URL, json={**VALID, "message": message})).status_code == 201
    rows = await db_query("SELECT message FROM contact_messages")
    assert rows[0][0] == message  # stored verbatim as data; clients must escape on output


async def test_missing_fields_and_extra_fields(client):
    assert (await client.post(URL, json={})).status_code == 422
    assert (await client.post(URL, json={"name": "Ada"})).status_code == 422
    assert (await client.post(URL, json={**VALID, "admin": True})).status_code == 422


async def test_malformed_json(client):
    response = await client.post(URL, content=b"{not json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


async def test_validation_errors_do_not_echo_submitted_values(client):
    secret = "super-secret-token-123"
    response = await client.post(URL, json={**VALID, "email": secret})
    assert response.status_code == 422
    assert secret not in response.text


async def test_rate_limit(client, db_query):
    for _ in range(5):
        assert (await client.post(URL, json=VALID)).status_code == 201
    blocked = await client.post(URL, json=VALID)
    assert blocked.status_code == 429
    assert blocked.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"
    assert int(blocked.headers["retry-after"]) > 0
    assert len(await db_query("SELECT 1 FROM contact_messages")) == 5


async def test_rate_limit_does_not_affect_read_endpoints(client):
    for _ in range(6):
        await client.post(URL, json=VALID)
    assert (await client.get("/api/v1/health")).status_code == 200


async def test_get_not_allowed_on_contact(client):
    response = await client.get(URL)
    assert response.status_code == 405
    assert response.json()["error"]["code"] == "METHOD_NOT_ALLOWED"
