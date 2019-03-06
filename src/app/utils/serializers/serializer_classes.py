import jsonpickle

from utils.logger_class import EventsAppLogger
from app.utils.serializers.serializer_response_classes import SingleEvent, SingleComment

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
        self.key = 'events'

    def serialize(self):
        temp_dict = {self.key:[]}
        event_list = list(map(lambda event: SingleEvent(event), self.objects))
        for event in event_list:
            temp_dict[self.key].append(event.__dict__)
            # temp_dict[event.id].pop('id')
        logger.debug(temp_dict)

        return jsonpickle.encode(temp_dict)


class EventParticipantsSerializer(BaseSerializer):
    def __init__(self, model, participants):
        super().__init__(model)
        self.participants = participants

    def serialize(self):
        id_list = list(map(lambda x: x.id.hex, list(self.participants)))
        return jsonpickle.encode(id_list)


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
