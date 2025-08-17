from auth.app.crud.user import get_user_by_email

class TestCrudFunctions:
    """Test crud functions"""

    async def test_crud_get_user_by_email(self, test_user1, auth_session):
        # create user
        auth_session.add(test_user1)
        await auth_session.flush()

        # get user by email
        user_by_email = await get_user_by_email(test_user1.email, auth_session)
        assert user_by_email == test_user1

    