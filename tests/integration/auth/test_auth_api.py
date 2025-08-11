import httpx

from tests.conftest import registrate_user
from auth.app.main import app


class TestAuthApi:
    """Testing auth api endpoints"""

    async def test_registration(self, test_user_data1, create_auth_db):
        """Test registration of user"""
        # correct registration
        response = await registrate_user(test_user_data1, app)

        assert response.status_code == 201
        assert "token" in response.json().keys()

        # duplicate registration (changed email, same login)
        data_same_by_login = test_user_data1.copy()
        data_same_by_login["email"] = "alfred12@email.com"
        response_same_login = await registrate_user(data_same_by_login, app)

        assert response_same_login.status_code == 409

        # duplicate registration (changed login, same email)
        data_same_by_email = test_user_data1.copy()
        data_same_by_email["login"] = "Alfred123"
        response_same_email = await registrate_user(data_same_by_email, app)

        assert response_same_email.status_code == 409

        # registration with different login and email
        data_changed_login_email = test_user_data1.copy()
        data_changed_login_email["login"] = "Alfred123"
        data_changed_login_email["email"] = "alfred12@email.com"
        response_changed_login_email = await registrate_user(data_changed_login_email, app)

        assert response_changed_login_email.status_code == 201
        assert "token" in response_changed_login_email.json().keys()
    

    async def test_login(self, test_user_data1, create_auth_db):
        """Test login with valid data"""
        # registrate user
        response_registration = await registrate_user(test_user_data1, app)

        # test correct login
        login_data_by_login = {"login": test_user_data1["login"], "password": test_user_data1["password"]}
        login_data_by_email = {"login": test_user_data1["email"], "password": test_user_data1["password"]}

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_by_login = await client.post("/auth/login/", json=login_data_by_login)
            response_by_email = await client.post("/auth/login/", json=login_data_by_email)
        
        assert response_by_login.status_code == 200
        assert response_by_email.status_code == 200

        assert "token" in response_by_email.json().keys()
        assert "token" in response_by_login.json().keys()

        # test wrong password
        login_data_wrong_password = {"login": test_user_data1["login"], "password": "wrongpassword"}

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_wrong_password = await client.post("/auth/login/", json=login_data_wrong_password)

        assert response_wrong_password.status_code == 401


    async def test_token_validation(self, test_user_data1, create_auth_db):
        """Test of token validation endpoint"""
        # correct token
        response_registration = await registrate_user(test_user_data1, app)

        data = response_registration.json()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_token_validation = await client.post("/auth/validate-token/", json=data)

        assert response_token_validation.status_code == 200
        assert "email" in response_token_validation.json().keys()

        # bad token
        data_expired_token = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkFsZXhIaXIyc2hAZW1haWwuY29tIiwiZXhwIjoxNzU0NTU1ODc1fQ.kHUwyPiMQBql-weDdZMsmz7inLfItv4LagE1s7cjnZY"}
        data_wrong_token = {"token": "wrong.token.really"}

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response_expired_token = await client.post("/auth/validate-token/", json=data_expired_token)
            response_wrong_token = await client.post("/auth/validate-token/", json=data_wrong_token)

        assert response_expired_token.status_code == 401
        assert response_wrong_token.status_code == 401

        