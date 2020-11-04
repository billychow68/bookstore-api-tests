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
