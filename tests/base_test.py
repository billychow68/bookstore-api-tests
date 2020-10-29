import requests
from requests.auth import HTTPBasicAuth
import uuid
import json


class BaseTest:

    base_url = "https://demoqa.com"

    def generate_username_password(self):
        """This method generates a random username and password and returns the data as a dict."""
        uuid_ = str(uuid.uuid4()).split('-', 1)[0].rstrip()
        username = "user-" + str(uuid_)
        password = "P@ss-" + str(uuid_)
        return {"userName": username, "password": password}

    def create_user(self, user):
        """This method calls the accounts create user endpoint and returns the response object."""
        url = self.base_url + '/Account/v1/User'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = user
        return requests.post(url, data=payload, json=headers)

    def delete_user_basic_auth(self, uuid_, user):
        """This method calls the deletion endpoint using basic auth and returns the response object."""
        url = self.base_url + '/Account/v1/User/' + uuid_
        auth = HTTPBasicAuth(user["userName"], user["password"])
        headers = {'Accept': "application/json"}
        return requests.delete(url, auth=auth, json=headers)

    def delete_user_token(self, uuid_, token):
        """This method calls the user deletion endpoint using a token and returns the response object. """
        url = self.base_url + '/Account/v1/User/' + uuid_
        headers = '{"Authorization": "Bearer ' + token + '", "Accept": "application/json"}'
        return requests.delete(url, headers=json.loads(headers))

    def generate_token(self, user):
        """This method calls the generate token endpoing and returns the response object."""
        url = self.base_url + '/Account/v1/GenerateToken'
        # todo: add headers
        return requests.post(url, user)
