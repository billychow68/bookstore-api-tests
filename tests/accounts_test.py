from tests.base_test import BaseTest
import pytest
import uuid


class TestAccountsAPI(BaseTest):

    def test_create_user_with_valid_input(self):
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        assert resp.status_code == 201
        assert resp_body["username"] == user["userName"]
        assert resp_body["userID"] != ""
        self.pprint_request(resp.request)
        self.pprint_response(resp)
        pass

    data1 = [[{"userName": "user123", "password": "abcdefgh"}, 400, 26],
             [{"userName": "user123", "password": "12345678"}, 400, 26],
             [{"userName": "user123", "password": "ABCDEFGH"}, 400, 26],
             [{"userName": "user123", "password": "aBcDeFgH"}, 400, 26],
             [{"userName": "user123", "password": ""}, 400, -1],
             [{"userName": "user123", "password": "Test!23"}, 400, 26],
             [{"userName": "user123", "password": "abcd1234"}, 400, 26],
             [{"userName": "user123", "password": "aBcD1234"}, 400, 26],
             [{"userName": "user123", "password": "!@#$%^&*"}, 400, 26],
             [{"password": "!@#$%^&*"}, 400, -1],
             [{"userName": "user123"}, 400, -1],
             [{"userName": "user123", "password": "Test1234"}, 400, 26],
             [{"userName": "", "password": "Test!234"}, 400, -1],
             [{}, 400, -1],
             [{"userName": "", "password": ""}, 400, -1]]

    @pytest.mark.parametrize("user, status_code, len_", data1)
    def test_create_user_with_invalid_input(self, user, status_code, len_):
        resp = self.create_user(user)
        assert resp.status_code == status_code
        assert resp.text.find("Passwords must have at least one non alphanumeric character") == len_
        self.pprint_request(resp.request)
        self.pprint_response(resp)
        pass

    def test_delete_existing_user_basic_auth(self):
        user = self.generate_username_password()
        resp = self.create_user(user)
        assert resp.status_code == 201
        resp_body = resp.json()
        self.pprint_request(resp.request)
        self.pprint_response(resp)
        resp2 = self.delete_user_basic_auth(resp_body["userID"], user)
        assert resp2.status_code == 204
        self.pprint_request(resp2.request)
        self.pprint_response(resp2)
        pass

    def test_delete_existing_user_token(self):
        user = self.generate_username_password()
        resp1 = self.create_user(user)
        assert resp1.status_code == 201
        resp_body1 = resp1.json()
        uuid_ = resp_body1["userID"]
        self.pprint_request(resp1.request)
        self.pprint_response(resp1)
        resp2 = self.generate_token(user)
        assert resp2.status_code == 200
        resp_body2 = resp2.json()
        token = resp_body2["token"]
        self.pprint_request(resp2.request)
        self.pprint_response(resp2)
        resp3 = self.delete_user_token(uuid_, token)
        assert resp3.status_code == 204
        self.pprint_request(resp3.request)
        self.pprint_response(resp3)
        pass

    def test_delete_user_with_invalid_uuid_basic_auth(self):
        user = self.generate_username_password()
        resp1 = self.create_user(user)
        assert resp1.status_code == 201
        self.pprint_request(resp1.request)
        self.pprint_response(resp1)
        uuid_ = str(uuid.uuid4())
        resp2 = self.delete_user_basic_auth(uuid_, user)
        assert resp2.status_code == 200
        assert resp2.text == '{"code":"1207","message":"User Id not correct!"}'
        self.pprint_request(resp2.request)
        self.pprint_response(resp2)
        pass
