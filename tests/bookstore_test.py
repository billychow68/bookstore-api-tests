from tests.base_test import BaseTest
import pytest
import uuid
import time
import json
import rootpath


class TestBookStoreAPI(BaseTest):
    """This class contains the test cases for the BookStore API."""

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

    data1 = ["9781449325862","9781449331818", "9781449337711","9781449365035",\
             "9781491904244","9781491950296","9781593275846","9781593277574"]

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