import httpx
from unittest.mock import patch

from tests.conftest import registrate_user
from auth.app.main import app as auth_app
from notes.app.main import app as notes_app


class TestNotesApi:
    "Testing notes api endpoints"

    async def create_note(self, test_user_data, test_note_data):
        # registrate user to which note will belong and getting token
        response_registration = await registrate_user(test_user_data, auth_app)

        # validate token with auth service to get user_id
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json=response_registration.json())

        # add user_id to which note will belong
        test_note_data["user_id"] = response_validate_token.json()["user_id"]

        mock_response = response_validate_token.json()

        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {response_registration.json()['token']}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response = await client.post("/notes/create/", json=test_note_data, headers=headers)

            return response


    async def test_create_notes(self, test_user_data1, test_note_data1, create_auth_db, create_notes_db):
        # create note with name and text
        response = await self.create_note(test_user_data1, test_note_data1)

        assert response.status_code == 201

        # # create note with only name
        # test_note_data_name = {"name": test_note_data1["name"]}
        # response_only_name = await self.create_note(test_user_data1, test_note_data_name)

        # assert response_only_name.status_code == 201

        # # create note with only text
        # test_note_data_text = {"text": test_note_data1["text"]}
        # response_only_text = await self.create_note(test_user_data1, test_note_data_text)

        # assert response_only_text.status_code == 422


    # async def test_list_of_notes(self, test_user_data1, test_note_data1, create_notes_db):
    #     self.create_note(test_user_data1, test_note_data1)

    #     async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
    #         response = await client.get("/notes/")

