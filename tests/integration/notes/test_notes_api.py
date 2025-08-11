import httpx

from tests.conftest import registrate_user
from auth.app.main import auth_app
from notes.app.main import notes_app

class TestNotesApi:
    "Testing notes api endpoints"

    async def create_note(self, test_user_data, test_notes_data):
        # registrate user to which note will belong
        response_registration = registrate_user(test_user_data, auth_app)

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json=response_registration)

        # add user_id to which note will belong
        test_notes_data["user_id"] = response_validate_token["user_id"]

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
            response = await client.post("/notes/create/", json=test_notes_data)


    async def test_create_notes(self, test_user_data1, test_notes_data1, test_notes_data2, create_notes_db):
        response 

    async def test_list_of_notes(self, test_user_data1, test_notes_data1, create_notes_db):
        self.create_note(test_user_data1, test_notes_data1)

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
            response = await client.get("/notes/")

