import unittest
import requests
import json


class IntegrationTests(unittest.TestCase):
    base_url = 'http://localhost:8000/api/'
    username = 'shide'
    password = '1234qwer'
    set_header = True

    def build_header(self):
        if self.set_header:
            data = {
                'username': self.username,
                'password': self.password
            }
            path = 'auth/login/'
            url = self.base_url + path

            res = requests.post(url, data=data)
            res = res.json()
            token = res['token']
            header = {
                'authorization': 'jwt ' + token
            }
        else:
            header = {}
        return header

    def test_token_validation(self):
        url2 = self.base_url + 'auth/testing/'
        header = self.build_header()
        res2 = requests.post(url2, headers=header)
        self.assertEqual(res2.status_code, 200, 'Valid token provided, request accepted')
        # self.assertEqual(reply, '"Token authentication works"', 'Valid token provided, request accepted')

    def test_request_without_token(self):
        url = self.base_url + 'auth/testing/'
        res2 = requests.post(url)
        reply = {
            'detail': 'Authentication credentials were not provided.'
        }
        self.assertEqual(res2.status_code, 401, 'No access allowed without token')
        #self.assertEqual(res2.json(), reply, 'No access allowed without token')

if __name__ == '__main__':
    unittest.main()