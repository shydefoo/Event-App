import jsonpickle

from utils.logger_class import EventsAppLogger
from app.utils.serializers.serializer_response_classes import SingleEvent, SingleComment, SingleUser

logger = EventsAppLogger(__name__).logger

class BaseSerializer:
    def __init__(self, model):
        self.model = model

    def serialize(self):
        pass

class EventSerializer(BaseSerializer):

    def __init__(self, model, objects):
        super().__init__(model)
        self.objects = objects
        self.key = 'event_list'

    def serialize(self):
        temp_dict = {self.key:[]}
        event_list = list(map(lambda event: SingleEvent(event), self.objects))
        for event in event_list:
            temp_dict[self.key].append(event.__dict__)
            # temp_dict[event.id].pop('id')
        logger.debug(temp_dict)
        self.context = temp_dict

        return jsonpickle.encode(temp_dict)


class UsersSerializer(BaseSerializer):
    def __init__(self, model, users):
        super().__init__(model)
        self.participants = users
        self.key = 'users'

    def serialize(self):
        temp_dict = {self.key:[]}
        user_list = list(map(lambda user: SingleUser(user), list(self.participants)))
        self.context = temp_dict
        for user in user_list:
            temp_dict[self.key].append(user.__dict__)
        logger.debug(temp_dict)
        return jsonpickle.encode(temp_dict)


class CommentsSerializer(BaseSerializer):
    def __init__(self, model, objects):
        super().__init__(model)
        self.objects = objects
        self.key = 'comments'

    def serialize(self):
        temp_dict = {self.key:[]}
        comment_list = list(map(lambda comment: SingleComment(comment), self.objects))
        for comment in comment_list:
            temp_dict[self.key].append(comment.__dict__)
            # temp_dict[comment.id].pop('id')
        logger.debug(temp_dict)
        return jsonpickle.encode(temp_dict)


class PhotoSerializer(BaseSerializer):
    def __init__(self, model, objects):
        self.objects = objects
        self.key = 'image_urls'

    def serialize(self):
        temp_dict= {self.key:[]}
        image_list = list(map(lambda image: image.image.url, self.objects))
        temp_dict[self.key].extend(image_list)
        return jsonpickle.encode(temp_dict)