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
                response_create_note = await client.post("/notes/create/", json=test_note_data, headers=headers)

            return response_create_note


    async def test_create_notes(self, test_user_data1, test_note_data1, test_note_data2, create_auth_db, create_notes_db):
        """Test creation of note"""
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create note with name and text
        response_create_note = await self.create_note(token, test_note_data1)

        assert response_create_note.status_code == 201
        
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
                response_list_of_notes = await client.get("/notes/", headers=headers)

        assert response_list_of_notes.status_code == 200
        assert len(response_list_of_notes.json()["notes"]) == 2
        assert response_list_of_notes.json()["notes"][0] is not None

    
    async def test_change_note(self, test_user_data1, test_note_data1, create_auth_db, create_notes_db):
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create note
        response_create_note = await self.create_note(token, test_note_data1)
        note_id = response_create_note.json()["id"]

        data_to_change = {
            "name": "New name",
        }

        # get validate token response for mock
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json={"token": token})
        mock_response = response_validate_token.json()

        # send a request to change note name
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_change_note = await client.put(f"/notes/{note_id}/", headers=headers, json=data_to_change)

        assert response_change_note.status_code == 200
        assert response_change_note.json()["id"] is not None
        assert response_change_note.json()["name"] == data_to_change["name"]

        # no data to change test
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_no_data = await client.put(f"/notes/{note_id}/", headers=headers, json={})
            
        assert response_no_data.status_code == 200
        assert response_no_data.json()["id"] is not None
        assert response_no_data.json()["name"] == data_to_change["name"]

        # same name to change test
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_no_data = await client.put(f"/notes/{note_id}/", headers=headers, json=data_to_change)
            
        assert response_no_data.status_code == 409

    
    async def test_get_note(self, test_user_data1, test_note_data1, create_auth_db, create_notes_db):
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create note
        response_create_note = await self.create_note(token, test_note_data1)
        note_id = response_create_note.json()["id"]

        # get validate token response for mock
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json={"token": token})
        mock_response = response_validate_token.json()

        # get note by id
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_get_note = await client.get(f"/notes/{note_id}/", headers=headers)

        assert response_get_note.status_code == 200
        assert response_get_note.json()["id"] is not None
        assert response_get_note.json()["name"] is not None

        # get note with wrong note_id
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_get_note_wrong_id = await client.get("/notes/123/", headers=headers)

        assert response_get_note_wrong_id.status_code == 404

    
    async def test_delete_note(self, test_user_data1, test_note_data1, create_auth_db, create_notes_db):
        # create user
        response_registration = await registrate_user(test_user_data1, auth_app)
        token = response_registration.json()["token"]

        # create note
        response_create_note = await self.create_note(token, test_note_data1)
        note_id = response_create_note.json()["id"]

        # get validate token response for mock
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=auth_app), base_url="http://test") as client:
            response_validate_token = await client.post("/auth/validate-token/", json={"token": token})
        mock_response = response_validate_token.json()

        # delete note by id
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_delete = await client.delete(f"/notes/{note_id}/", headers=headers)

        assert response_delete.status_code == 204

        # check is note could be accessed 
        with patch("notes.app.services.notes.validate_token") as mock_validate:
            mock_validate.return_value = mock_response

            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=notes_app), base_url="http://test") as client:
                response_get_note = await client.get(f"/notes/{note_id}/", headers=headers)

        assert response_get_note.status_code == 404
        




