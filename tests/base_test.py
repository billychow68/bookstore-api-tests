import requests
from requests.auth import HTTPBasicAuth
import uuid
import json


class BaseTest:

    base_url = "https://demoqa.com"

    def name_test(self, name):
        print(name)

    def generate_username_password(self):
        """This method generates a random username and password and returns the data as a dict."""
        print("[TEST STEP][BaseTest::generate_username_password]")
        uuid_ = str(uuid.uuid4()).split('-', 1)[0].rstrip()
        username = "user-" + str(uuid_)
        password = "P@ss-" + str(uuid_)
        return {"userName": username, "password": password}

    def create_user(self, user):
        """This method calls the account create user endpoint and returns the response object."""
        print("[TEST STEP][BaseTest::create_user]")
        url = self.base_url + '/Account/v1/User'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = user
        return requests.post(url, data=payload, json=headers)

    def delete_user_basic_auth(self, uuid_, user):
        """This method calls the account delete user endpoint using basic auth and returns the response object."""
        print("[TEST STEP][BaseTest::delete_user_basic_auth]")
        url = self.base_url + '/Account/v1/User/' + uuid_
        auth = HTTPBasicAuth(user["userName"], user["password"])
        headers = {'Accept': "application/json"}
        return requests.delete(url, auth=auth, json=headers)

    def delete_user_token(self, uuid_, token):
        """This method calls the account delete user endpoint using a token and returns the response object. """
        print("[TEST STEP][BaseTest::delete_user_token]")
        url = self.base_url + '/Account/v1/User/' + uuid_
        headers = '{"Authorization": "Bearer ' + token + '", "Accept": "application/json"}'
        return requests.delete(url, headers=json.loads(headers))

    def generate_token(self, user):
        """This method calls the account generate token endpoint and returns the response object."""
        print("[TEST STEP][BaseTest::generate_token]")
        url = self.base_url + '/Account/v1/GenerateToken'
        # todo: add headers
        return requests.post(url, user)

    def get_user_basic_auth(self, uuid_, user):
        """This method will return the user using basic auth."""
        print("[TEST STEP][BaseTest::get_user_basic_auth]")
        url = self.base_url + '/Account/v1/User/' + uuid_
        auth = HTTPBasicAuth(user["userName"], user["password"])
        headers = {'Accept': "application/json"}
        return requests.get(url, auth=auth, json=headers)

    def get_user_token(self, uuid_, token):
        pass

    def get_books(self):
        """This method will return all books available."""
        print("[TEST STEP][BaseTest::get_books]")
        url = self.base_url + '/BookStore/v1/Books'
        headers = {'Content-Type': "application/json"}
        return requests.get(url, json=headers)

    def get_book_by_isbn(self, isbn):
        """This method will return a book by ISBN."""
        print("[TEST STEP][BaseTest::get_book_by_isbn]")
        url = self.base_url + '/BookStore/v1/Book?ISBN=' + isbn
        headers = {'Content-Type': "application/json"}
        return requests.get(url, json=headers)

    def is_book_in_books(self, book, books):
        """This method will return True if the 'book' is in the list of 'books', otherwise False."""
        print("[TEST STEP][BaseTest::is_book_in_books]")
        len_ = len(books)
        for b in range(len_):
            if book["isbn"] == books[b]["isbn"]:
                if book == books[b]:
                    return True
        return False

    def add_books_to_user_collection(self, user, books):
        """This method will add a book to the user's collection."""
        print("[TEST STEP][BaseTest::add_books_to_user_collection]")
        url = self.base_url + '/BookStore/v1/Books'
        headers = {'Content-Type': "application/json"}
        auth = HTTPBasicAuth(user["userName"], user["password"])
        return requests.post(url, json=books, headers=headers, auth=auth)

    def delete_books_from_user_collection(self, uuid_, user):
        """This method will delete all books from the user's collection."""
        print("[TEST STEP][BaseTest::delete_books_from_user_collection]")
        url = self.base_url + '/BookStore/v1/Books?UserId=' + uuid_
        auth = HTTPBasicAuth(user["userName"], user["password"])
        return requests.delete(url, auth=auth)

    def delete_a_book_from_user_collection(self, isbn, uuid_, user):
        """This method will delete a book from the user's collection."""
        print("[TEST STEP][BaseTest::delete_a_book_from_user_collection]")
        url = self.base_url + '/BookStore/v1/Book'
        payload = dict({"isbn": isbn, "userId": uuid_})
        auth = HTTPBasicAuth(user["userName"], user["password"])
        return requests.delete(url, auth=auth, json=payload)

    def replace_book(self, cur_isbn, new_isbn, uuid_, user):
        """This method will update the user's collection by replacing the current book (ISBN) with the new book (ISBN)."""
        print("[TEST STEP][BaseTest::replace_book]")
        url = self.base_url + '/BookStore/v1/Books/' + cur_isbn
        payload = dict({"userId": uuid_, "isbn": new_isbn})
        auth = HTTPBasicAuth(user["userName"], user["password"])
        return requests.put(url, auth=auth, json=payload)

    def pprint_request(self, request):
        """This method will pretty print the Request object to HTML report."""
        print('\n{}\n{}\n\n{}\n\n{}\n'.format(
            '---------------- request -----------------',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            request.body)
        )

    def pprint_response(self, resp):
        """This method will pretty print the Response object to HTML report."""
        print('\n{}\n{}\n\n{}\n\n{}\n'.format(
            '---------------- response ----------------',
            str(resp.status_code) + ' ' + str(resp.reason) + ' ' + str(resp.url),
            '\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items()),
            resp.text)
        )
