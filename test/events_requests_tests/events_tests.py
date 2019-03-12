import pprint

from test.requests_test import IntegrationTests
import requests

class EventsTests(IntegrationTests):
    base_url = 'http://localhost:8000/api/'
    # base_url = 'http://203.116.180.244/api/'
    # username = 'admin'
    # password = '1234qwer'
    event_id = 'ff903156-cfc8-4e93-869b-227405624cb0'
    user_id = 'ccd4e975-9608-412c-acf2-5150caaef1b3'
    def test_get_events(self):
        url = self.base_url + 'get_events/'
        header = self.build_header()
        # header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_get_photos(self):
        url = self.base_url + 'get_photos_by_event/{}'.format(self.event_id)

        header = self.build_header()
        # header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_join_event(self):
        url = self.base_url + 'join_event/'
        header = self.build_header()
        # header = {}
        data = {
            'event_id':self.event_id,
            'user_id':self.user_id
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_like_event(self):
        url = self.base_url + 'like_event/'
        header = self.build_header()
        # header = {}
        data = {
            'event_id':self.event_id,
            'user_id':self.user_id
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_leave_event(self):
        url = self.base_url + 'leave_event/'
        header = self.build_header()
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_comment_on_event(self):
        url = self.base_url + 'comment_event/'
        header = self.build_header()
        # header = {}
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'comment': 'testing123'
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_get_event_comments(self):
        url = self.base_url + 'get_event_comments/{}'.format(self.event_id)
        header = self.build_header()
        # header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_search_event(self):
        url = self.base_url + 'search_event/'
        header = self.build_header()
        search_text = ''
        data = {
            'search_text' : search_text
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_get_event_participants(self):
        url = self.base_url + 'get_event_participants/{}'.format(self.event_id)
        header = self.build_header()
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_get_event_likes(self):
        url = self.base_url + 'get_event_likes/{}'.format(self.event_id)
        header = self.build_header()
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_get_event_photos(self):
        url = self.base_url + 'get_event_photos/{}'.format(self.event_id)
        header = self.build_header()
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_create_user(self):
        url = self.base_url + 'create_user/'
        header = self.build_header()
        new_user = 'new_user'
        password = 'qwerty'
        is_staff = 0
        data = {
            'username': new_user,
            'password': password,
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.json())

        url2 = self.base_url + 'get_jwt_token/'
        res = requests.post(url2, data=data)
        pprint.pprint(res.json())

    def test_create_category(self):
        url = self.base_url + 'create_category/'
        header = self.build_header()
        data = {
            'category': 'Sports'
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.json())




