import pprint

from test.requests_test import IntegrationTests
import requests

class EventsTests(IntegrationTests):
    event_id = '6db48338-8a06-4717-b79f-e705b4da26d1'
    user_id = '8ad8afc4-2870-4264-892a-ac5acb7ddc68'
    def test_get_events(self):
        url = self.base_url + 'get_events/'
        # header = self.build_header()
        header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_get_photos(self):
        url = self.base_url + 'get_photos_by_event/{}'.format(self.event_id)

        # header = self.build_header()
        header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())

    def test_join_event(self):
        url = self.base_url + 'join_event/'
        # header = self.build_header()
        header = {}
        data = {
            'event_id':self.event_id,
            'user_id':self.user_id
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_like_event(self):
        url = self.base_url + 'like_event/'
        # header = self.build_header()
        header = {}
        data = {
            'event_id':self.event_id,
            'user_id':self.user_id
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_comment_on_event(self):
        url = self.base_url + 'like_event/'
        # header = self.build_header()
        header = {}
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'comment': 'Hello hello'
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)