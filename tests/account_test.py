import pytest
import uuid
from tests.base_test import BaseTest


class TestAccountAPI(BaseTest):
    """This class contains the test cases for Account API."""

    def test_create_user_with_valid_input(self):
        """This test case will create a user with valid input."""
        # setup
        user = self.generate_username_password()

        # test
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # teardown:
        resp2 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp2.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

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
        """This test case will attempt to create users with invalid input."""
        # setup: none

        # test
        resp = self.create_user(user)
        try:
            assert resp.status_code == status_code
            assert resp.text.find("Passwords must have at least one non alphanumeric character") == len_
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # teardown: none

    def test_delete_existing_user_with_valid_input_using_basic_auth(self):
        """This test case will delete a valid user using Basic Auth."""
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        try:
            assert resp.status_code == 201
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        resp_body = resp.json()

        # test
        resp2 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp2.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # teardown: none

    def test_delete_existing_user_with_valid_input_using_token(self):
        """This test case will delete a valid user using a token."""
        # setup
        user = self.generate_username_password()
        resp1 = self.create_user(user)
        try:
            assert resp1.status_code == 201
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp1.request)
            self.pprint_response(resp1)
        resp_body1 = resp1.json()
        uuid_ = resp_body1["userID"]
        resp2 = self.generate_token(user)
        try:
            assert resp2.status_code == 200
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)
        resp_body2 = resp2.json()
        token = resp_body2["token"]

        # test
        resp3 = self.delete_user_token(uuid_, token)
        try:
            assert resp3.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp3.request)
            self.pprint_response(resp3)

        # teardown: none

    def test_delete_user_with_invalid_uuid_using_basic_auth(self):
        """This test case will attempt to delete a user with an invalid UUID using Basic Auth."""
        # setup
        user = self.generate_username_password()
        resp1 = self.create_user(user)
        resp_body1 = resp1.json()
        try:
            assert resp1.status_code == 201
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp1.request)
            self.pprint_response(resp1)
        uuid_ = str(uuid.uuid4())

        # test
        resp2 = self.delete_user_basic_auth(uuid_, user)
        try:
            assert resp2.status_code == 200
            assert resp2.text == '{"code":"1207","message":"User Id not correct!"}'
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # teardown
        resp3 = self.delete_user_basic_auth(resp_body1["userID"], user)
        try:
            assert resp3.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp3.request)
            self.pprint_response(resp3)
