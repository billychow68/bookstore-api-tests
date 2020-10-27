import requests
from requests.auth import HTTPBasicAuth
import uuid


class BaseTest:

    base_url = "https://demoqa.com"

    def new_user(self):
        id = str(uuid.uuid4()).split('-',1)[0].rstrip()
        username = "user-" + str(id)
        password = "P@ss-" + str(id)
        print(username, password)
        return [username, password]

    def delete_user_basic_auth(self, uuid, user, password):
        url = self.base_url + '/Account/v1/User/' + uuid
        auth = HTTPBasicAuth(user, password)
        r = requests.delete(url, auth=auth)
        return dict({"status_code": r.status_code, "ok": r.ok, "text": r.text})

    # def delete_user_token(uuid, token):
    #     url = base_url + '/Account/v1/User/' + uuid
    #     headers = f'\{"Authorization": "Bearer {token}"\}'
    #     r = requests.delete(url, headers)
    #     pass

    def create_user(self, user):
        url = self.base_url + '/Account/v1/User'
        payload = dict({"userName": user[0], "password": user[1]})
        # headers = {'Content-Type':'application/json', 'Accept':'application/json'}
        r = requests.post(url, data=payload)
        return dict({"status_code": r.status_code, "ok": r.ok, "text": r.text})



