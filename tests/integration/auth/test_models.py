import uuid

from auth.app.models import User

class TestUserModel:
    """Test user model"""

    async def test_user_id_generation(self, test_user1, test_user2, auth_session):
        """Test that user ID is automatically generated as UUID"""
        auth_session.add(test_user1)
        auth_session.add(test_user2)
        await auth_session.flush()

        # Each user should get a unique UUID
        assert isinstance(test_user1.id, uuid.UUID)
        assert isinstance(test_user2.id, uuid.UUID)
        assert test_user1.id != test_user2.id

    

