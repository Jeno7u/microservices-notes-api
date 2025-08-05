from auth.app.models import User
from auth.app.crud.user import get_user_by_email

class TestCrudFunctions:
    """Test crud functions"""

    async def test_crud_get_user_by_email(self, auth_session):
        # user creation
        user = User(login="user", name="Test", surname="User", email="test@example.com", password="hash", is_admin=False)
        auth_session.add(user)
        await auth_session.flush()

        # user by email
        user_by_email = await get_user_by_email("test@example.com", auth_session)
        assert user_by_email == user

    