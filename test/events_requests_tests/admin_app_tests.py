import requests

from test.requests_test import IntegrationTests


class AdminAppTest(IntegrationTests):

    admin_url = 'http://localhost:8000/admin_dashboard/'
    def test_home_app(self):
        url_path = self.admin_url
        header = self.build_header()
        res = requests.get(url_path, headers=header)
        print(res.text)