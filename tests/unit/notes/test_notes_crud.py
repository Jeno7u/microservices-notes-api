from notes.app.models import Note
from notes.app.crud.note import (
    get_note_by_user_and_name,
    get_note_by_id
    )

class TestCrudFunctions:
    """Test crud functions"""
    async def create_note(self, test_note_data, notes_session, user_id="d3c3a3e7-9613-452a-9d9f-31d2cfb0db96"): # random base uuid
        note = Note(
            name=test_note_data["name"], 
            text=test_note_data["text"],
            user_id=user_id
        )
        notes_session.add(note)
        return note

    async def test_get_note_by_user_and_name(self, test_note_data1, notes_session):
        # create note
        note = await self.create(test_note_data1, notes_session)
        await notes_session.flush()

        # get note by user and name
        note_by_user_and_name = await get_note_by_user_and_name(notes_session, user_id, test_note_data1["name"])
        assert note_by_user_and_name == note

    
    async def test_get_note_by_id(self, test_note_data1, notes_session):
        # create note
        note = await self.create(test_note_data1, notes_session)
        await notes_session.flush()

        # get note by id
        note_by_id = await get_note_by_id(notes_session, note.id)
        assert note_by_id == note


    # async def test_generate_unique_name(self, test_note_data1, notes_session):



    # async def test_crud_get_user_by_email(self, test_user1, auth_session):
    #     # create user
    #     auth_session.add(test_user1)
    #     await auth_session.flush()

    #     # user by email
    #     user_by_email = await get_user_by_email(test_user1.email, auth_session)
    #     assert user_by_email == test_user1

    