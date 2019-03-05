import pprint

from test.requests_test import IntegrationTests
import requests

class EventsTests(IntegrationTests):
    base_url = 'http://localhost:8000/api/'
    event_id = '6dbe4ec4-7caa-4b9a-aeef-41ad67a963c7'
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

    def test_comment_on_event(self):
        url = self.base_url + 'comment_event/'
        header = self.build_header()
        # header = {}
        data = {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'comment': 'omg'
        }
        res = requests.post(url, headers=header, data=data)
        pprint.pprint(res.text)

    def test_get_event_comments(self):
        url = self.base_url + 'get_event_comments/{}'.format(self.event_id)
        header = self.build_header()
        # header = {}
        res = requests.get(url, headers=header)
        pprint.pprint(res.json())