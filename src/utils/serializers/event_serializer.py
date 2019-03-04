import jsonpickle

from utils.logger_class import EventsAppLogger

logger = EventsAppLogger(__name__).logger

class BaseSerializer:
    def __init__(self, model):
        self.model = model

    def serialize(self):
        pass


class _single_event:
    def __init__(self, event):
        self.date = event.date.strftime('%d-%m-%y')
        self.description = event.description
        self.title = event.title
        self.id = event.id.hex
        self.likes = list(map(self.extract_id, list(event.likes.all())))
        self.participants = list(map(self.extract_id, list(event.participants.all())))

    def extract_id(self, object):
        return object.id.hex


class EventSerializer(BaseSerializer):

    def __init__(self, model, objects):
        super().__init__(model)
        self.objects = objects

    def serialize(self):
        temp_dict = {}
        event_list = list(map(lambda event: _single_event(event), self.objects))
        for event in event_list:
            temp_dict[event.id] = event.__dict__
            temp_dict[event.id].pop('id')
        logger.debug(temp_dict)

        return jsonpickle.encode(temp_dict)


class EventParticipantsSerializer(BaseSerializer):
    def __init__(self, model, participants):
        super().__init__(model)
        self.participants = participants

    def serialize(self):
        id_list = list(map(lambda x: x.id.hex, list(self.participants)))
        return jsonpickle.encode(id_list)
