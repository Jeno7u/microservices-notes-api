import httpx

from auth.app.main import app


class TestAuthApi:
    """Testing auth api endpoints"""

    async def registrate_user(self, test_user_data1):
        """Registrating user"""
        register_data = test_user_data1.copy()
        register_data.pop("is_admin")

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/auth/register/", json=register_data)
            
        return response


    async def test_registration(self, test_user_data1, create_auth_db):
        """Test registration of user"""
        response = await self.registrate_user(test_user_data1)

        assert response.status_code == 201
        assert "token" in response.json().keys()
    

    async def test_login(self, test_user_data1, create_auth_db):
        """Test login with valid data"""
        response_registration = await self.registrate_user(test_user_data1)

        login_data_by_login = {"login": test_user_data1["login"], "password": test_user_data1["password"]}
        login_data_by_email = {"login": test_user_data1["email"], "password": test_user_data1["password"]}

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_by_login = await client.post("/auth/login/", json=login_data_by_login)
            response_by_email = await client.post("/auth/login/", json=login_data_by_email)
        
        assert response_by_login.status_code == 200
        assert response_by_email.status_code == 200

        assert "token" in response_by_email.json().keys()
        assert "token" in response_by_login.json().keys()

    async def test_token_validation(self, test_user_data1, create_auth_db):
        """Test of token validation endpoint"""
        response_registration = await self.registrate_user(test_user_data1)

        data = response_registration.json()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_token_validation = await client.post("/auth/validate-token/", json=data)

        assert response_token_validation.status_code == 200
        assert "email" in response_token_validation.json().keys()
