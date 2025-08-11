import uuid

from notes.app.models import Note


class TestNotesModel:
    """Test notes model"""

    async def test_user_id_generation(self, test_notes_data1, test_notes_data2, notes_session):
        """Test that notes ID is automatically generated as UUID"""
        test_note1 = Note(
            name=test_notes_data1["name"], 
            text=test_notes_data1["text"],
            user_id="d3c3a3e7-9613-452a-9d9f-31d2cfb0db96" # random uuid
        )
        test_note2 = Note(
            name=test_notes_data2["name"], 
            text=test_notes_data2["text"],
            user_id="7a782a81-7be5-4eab-ac0c-6bc113f4e10d" # random uuid
        )

        notes_session.add(test_note1)
        notes_session.add(test_note2)
        await notes_session.flush()

        # Each note should get a unique UUID
        assert isinstance(test_note1.id, uuid.UUID)
        assert isinstance(test_note2.id, uuid.UUID)
        assert test_note1.id != test_note2.id

    

