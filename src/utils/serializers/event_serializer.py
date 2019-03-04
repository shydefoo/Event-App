import jsonpickle


class BaseSerializer:
    def __init__(self, model):
        self.model = model

    def serialize(self):
        pass


class EventSerializer(BaseSerializer):
    def __init__(self, model, objects):
        super().__init__(model)
        self.objects = objects

    def serialize(self):
        self.contents = {self.model: []}
        for object in self.objects:
            self.contents[self.model].append(object.__dict__)
        print(self.contents)
        return jsonpickle.encode(self.contents)
