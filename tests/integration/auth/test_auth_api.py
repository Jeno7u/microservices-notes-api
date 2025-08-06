import httpx


from auth.app.main import app

class TestAuthApi:
    """Testing auth api endpoints"""

    async def test_registration(self, test_user_data1):
        register_data = test_user_data1.pop("is_admin")

        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/auth/register/", json=register_data)

        assert response.status_code == 201
    
    # async def test_login(self, test_user_data1, test_user1, auth_session):
    #     """Test login """
    #     auth_session.
    #     login_data_by_login = {"login": test_user_data1["login"], "password": test_user_data1["password"]}
    #     login_data_by_email = {"login": test_user_data1["email"], "password": test_user_data1["password"]}

    #     async with httpx.AsyncClient(app=app, base_url="http://test") as client:
    #         response_by_login = await client.post("/auth/login/", json=login_data_by_login)
    #         response_by_email = await client.post("/auth/login/", json=login_data_by_email)
        
    #     assert response_by_login.status_code == 200
    #     assert response_by_email.status_code == 200
