from tests.base_test import BaseTest
import pytest
import json
import uuid


class TestAccounts(BaseTest):

    def test_create_account_with_valid_password(self):
        user = self.new_user()
        res = self.create_user(user)
        assert res["status_code"] == 201
        pass

    data1 = [["user123", "abcdefgh", 400, 26],
             ["user123", "12345678", 400, 26],
             ["user123", "ABCDEFGH", 400, 26],
             ["user123", "aBcDeFgH", 400, 26],
             ["user123", "", 400, -1],
             ["user123", "abcd1234", 400, 26],
             ["user123", "aBcD1234", 400, 26],
             ["user123", "!@#$%^&*", 400, 26],
             ["user123", "Test1234", 400, 26],
             ["", "Test!234", 400, -1],
             ["", "", 400, -1]]

    @pytest.mark.parametrize("user, password, status_code, len", data1)
    def test_create_account_with_invalid_password(self, user, password, status_code, len):
        res = self.create_user([user, password])
        assert res["status_code"] == status_code
        assert res["text"].find("Passwords must have at least one non alphanumeric character") == len
        pass

    def test_delete_existing_account(self):
        user = self.new_user()
        res = self.create_user(user)
        assert res["status_code"] == 201
        temp = json.loads(res["text"])
        res = self.delete_user_basic_auth(temp["userID"], user[0], user[1])
        assert res["status_code"] == 204
        pass

    def test_delete_account_with_invalid_uuid(self):
        user = self.new_user()
        res = self.create_user(user)
        assert res["status_code"] == 201
        id = str(uuid.uuid4())
        res = self.delete_user_basic_auth(id, user[0], user[1])
        assert res["status_code"] == 200
        assert res["text"] == '{"code":"1207","message":"User Id not correct!"}'
        pass
