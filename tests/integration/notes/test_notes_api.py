import httpx
from unittest.mock import patch

from tests.conftest import registrate_user
from auth.app.main import app as auth_app
from notes.app.main import app as notes_app


class TestNotesApi:
    "Testing notes api endpoints"

    async def create_note(self, token, test_note_data):
        # validate token with auth service to get user_id
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json={"token": token})

        # add user_id to which note will belong
        test_note_data["user_id"] = response_validate_token.json()["user_id"]

        mock_response = response_validate_token.json()

        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response = await client.post("/notes/create/", json=test_note_data, headers=headers)

            return response


    async def test_create_notes(self, test_user_data1, test_note_data1, test_note_data2, create_auth_db, create_notes_db):
        """Test creation of note"""
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create note with name and text
        response = await self.create_note(token, test_note_data1)

        assert response.status_code == 201
        
        # create note with same name
        test_note_data_same_name = {"name": test_note_data1["name"]}
        response_same_name = await self.create_note(token, test_note_data_same_name)

        assert response_same_name.status_code == 409

        # create note with only name
        test_note_data_name = {"name": test_note_data2["name"]}
        response_only_name = await self.create_note(token, test_note_data_name)

        assert response_only_name.status_code == 201

        # create note with only text
        test_note_data_text = {"text": test_note_data1["text"]}
        response_only_text = await self.create_note(token, test_note_data_text)
        assert response_only_text.status_code == 201


    async def test_list_of_notes(self, test_user_data1, test_note_data1, test_note_data2, create_auth_db, create_notes_db):
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create notes
        await self.create_note(token, test_note_data1)
        await self.create_note(token, test_note_data2)

        # get validate token response for mock
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json={"token": token})
        mock_response = response_validate_token.json()

        # get list of notes that belongs to user
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response = await client.get("/notes/", headers=headers)

            return response

        assert response.status_code == 200

