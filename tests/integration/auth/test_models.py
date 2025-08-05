import uuid

from auth.app.models import User

class TestUserModel:
    """Test user model"""

    async def test_user_id_generation(self, auth_session):
        """Test that user ID is automatically generated as UUID"""
        user1 = User(login="user1", name="Test", surname="User", email="test1@example.com", password="hash", is_admin=False)
        user2 = User(login="user2", name="Test", surname="User", email="test2@example.com", password="hash", is_admin=False)

        auth_session.add(user1)
        auth_session.add(user2)
        await auth_session.flush()

        # Each user should get a unique UUID
        assert isinstance(user1.id, uuid.UUID)
        assert isinstance(user2.id, uuid.UUID)
        assert user1.id != user2.id

    

