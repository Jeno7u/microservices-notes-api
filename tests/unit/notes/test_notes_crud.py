from notes.app.models import Note
from notes.app.crud.note import (
    get_note_by_user_and_name,
    get_note_by_id,
    generate_unique_name
    )


USER_ID = "d3c3a3e7-9613-452a-9d9f-31d2cfb0db96" # random uuid

class TestCrudFunctions:
    """Test crud functions"""
    async def create_note(self, test_note_data, notes_session, user_id=USER_ID):
        note = Note(
            name=test_note_data["name"], 
            text=test_note_data["text"],
            user_id=user_id
        )
        notes_session.add(note)
        return note

    async def test_get_note_by_user_and_name(self, test_note_data1, notes_session):
        # create note
        note = await self.create_note(test_note_data1, notes_session, USER_ID)
        await notes_session.flush()

        # get note by user and name
        note_by_user_and_name = await get_note_by_user_and_name(notes_session, USER_ID, test_note_data1["name"])
        assert note_by_user_and_name == note

    
    async def test_get_note_by_id(self, test_note_data1, notes_session):
        # create note
        note = await self.create_note(test_note_data1, notes_session)
        await notes_session.flush()

        # get note by id
        note_by_id = await get_note_by_id(notes_session, note.id)
        assert note_by_id == note


    async def test_generate_unique_name(self, test_note_data1, test_note_data2, notes_session):
        base_name = "New Note"
        # create notes with normal name
        note_normal_name1 = await self.create_note(test_note_data1, notes_session, USER_ID)
        note_normal_name2 = await self.create_note(test_note_data2, notes_session, USER_ID)
        await notes_session.flush()

        # get generated unique name
        new_name = await generate_unique_name(notes_session, USER_ID, base_name)
        assert new_name == "New Note 1"

        # create notes with base name
        note_base_name1 = await self.create_note({"name": "New Note 1", "text": None}, notes_session, USER_ID)
        note_base_name2 = await self.create_note({"name": "New Note 2", "text": None}, notes_session, USER_ID)

        new_name = await generate_unique_name(notes_session, USER_ID, base_name)
        assert new_name == "New Note 3"