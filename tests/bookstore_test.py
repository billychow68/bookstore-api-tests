from tests.base_test import BaseTest
import pytest
import uuid
import json
import rootpath


class TestBookStoreAPI(BaseTest):
    """This class contains the test cases for the BookStore API."""

    @pytest.mark.smoketest
    def test_get_books(self):
        """This test case will retrieve the books."""
        # setup
        root_path = rootpath.detect()
        with open(root_path + "/tests/books.json") as f:
            data = json.load(f)

        # test
        resp = self.get_books()
        resp_body = resp.json()
        try:
            assert resp.status_code == 200
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["books"] == data["books"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # teardown: none

    data1 = ["9781449325862", "9781449331818", "9781449337711", "9781449365035",
             "9781491904244", "9781491950296", "9781593275846", "9781593277574"]

    @pytest.mark.parametrize("isbn", data1)
    def test_get_book_with_valid_isbn(self, isbn):
        """This test case will retrieve a book with a valid ISBN."""
        # setup
        root_path = rootpath.detect()
        with open(root_path + "/tests/books.json") as f:
            data = json.load(f)

        # test
        resp = self.get_book_by_isbn(isbn)
        resp_body = resp.json()
        try:
            assert resp.status_code == 200
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert self.is_book_in_books(resp_body, data["books"])
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # teardown: none

    def test_get_book_with_invalid_isbn(self):
        """This test case will attempt to retrieve a book with an invalid ISBN."""
        # setup
        uuid_ = str(uuid.uuid4())

        # test
        resp = self.get_book_by_isbn(uuid_)
        resp_body = resp.json()
        try:
            assert resp.status_code == 400
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["code"] == "1205"
            assert resp_body["message"] == "ISBN supplied is not available in Books Collection!"
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # teardown: none

    data2 = '{"userId": "", "collectionOfIsbns": [{"isbn": "9781449325862"}]}'

    @pytest.mark.smoketest
    def test_add_1_book_to_user_collection(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # test
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # teardown
        resp3 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp3.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp3.request)
            self.pprint_response(resp3)

    data3 = '{"userId": "", "collectionOfIsbns": [{"isbn": "1234567890123"}]}'

    def test_add_book_with_invalid_isbn_to_user_collection(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)

        # test
        data = json.loads(self.data3)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 400
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body2["code"] == "1205"
            assert resp_body2["message"] == "ISBN supplied is not available in Books Collection!"
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # teardown
        resp3 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp3.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp3.request)
            self.pprint_response(resp3)

    @pytest.mark.smoketest
    def test_delete_books_from_user_collection(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        resp3 = self.delete_books_from_user_collection(resp_body["userID"], user)
        assert resp3.status_code == 204
        assert resp3.text == ''

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    def test_delete_books_from_user_collection_failure_due_to_invalid_userid(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        resp3 = self.delete_books_from_user_collection("1234567890", user)
        resp_body3 = resp3.json()
        assert resp3.status_code == 401
        assert resp_body3["code"] == "1207"
        assert resp_body3["message"] == "User Id not correct!"

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    @pytest.mark.smoketest
    def test_delete_a_book_from_user_collection(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        resp3 = self.delete_a_book_from_user_collection(resp_body2["books"][0]["isbn"], resp_body["userID"], user)
        assert resp3.status_code == 204

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    def test_delete_a_book_from_user_collection_failure_due_to_invalid_isbn(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        resp3 = self.delete_a_book_from_user_collection("1234567890", resp_body["userID"], user)
        resp_body3 = resp3.json()
        assert resp3.status_code == 400
        assert resp_body3["code"] == "1206"
        assert resp_body3["message"] == "ISBN supplied is not available in User's Collection!"

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    @pytest.mark.smoketest
    def test_replace_book(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        new_isbn = "9781449331818"
        resp3 = self.replace_book(resp_body2["books"][0]["isbn"], new_isbn, resp_body["userID"], user)
        resp_body3 = resp3.json()
        assert resp3.status_code == 200
        assert resp_body3["books"][0]["isbn"] == new_isbn

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    def test_replace_book_failure_due_to_invalid_source_isbn(self):
        # setup
        user = self.generate_username_password()
        resp = self.create_user(user)
        resp_body = resp.json()
        try:
            assert resp.status_code == 201
            assert resp.headers["Content-Type"] == "application/json; charset=utf-8"
            assert resp_body["username"] == user["userName"]
            assert resp_body["userID"] != ""
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp.request)
            self.pprint_response(resp)
        data = json.loads(self.data2)
        data["userId"] = resp_body["userID"]
        resp2 = self.add_books_to_user_collection(user, data)
        resp_body2 = resp2.json()
        try:
            assert resp2.status_code == 201
            assert resp2.headers["Content-Type"] == "application/json; charset=utf-8"
            # todo: rewrite to assert on dicts, not ISBNs
            assert resp_body2["books"][0]["isbn"] == data["collectionOfIsbns"][0]["isbn"]
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp2.request)
            self.pprint_response(resp2)

        # test
        new_isbn = "9781449331818"
        resp3 = self.replace_book("1234567890", new_isbn, resp_body["userID"], user)
        resp_body3 = resp3.json()
        assert resp3.status_code == 400
        assert resp_body3["code"] == "1206"
        assert resp_body3["message"] == "ISBN supplied is not available in User\'s Collection!"

        # teardown
        resp4 = self.delete_user_basic_auth(resp_body["userID"], user)
        try:
            assert resp4.status_code == 204
        except AssertionError:
            raise
        finally:
            self.pprint_request(resp4.request)
            self.pprint_response(resp4)

    @pytest.mark.skip(reason="Needs implementation.")
    def test_replace_book_failure_due_to_invalid_dest_isbn(self):
        pass
