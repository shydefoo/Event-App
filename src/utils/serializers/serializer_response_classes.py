class BaseSingleEntity:
    def __init__(self):
        pass

    def extract_id(self, object):
        return object.id.hex

class SingleEvent(BaseSingleEntity):
    def __init__(self, event):
        self.date = event.date.strftime('%d-%m-%y')
        self.description = event.description
        self.title = event.title
        self.category = list(map(self.extract_category, list(event.category.all())))
        self.id = self.extract_id(event)
        self.likes = list(map(self.extract_id, list(event.likes.all())))
        self.participants = list(map(self.extract_id, list(event.participants.all())))

    # def extract_id(self, object):
    #     return object.id.hex
    def extract_category(self, category):
        return category.category

class SingleComment(BaseSingleEntity):
    def __init__(self, comment):
        self.date = comment.date.strftime('%d-%m-%y')
        self.comment = comment.comment
        self.id = comment.id.hex
        self.user = self.extract_id(comment.user)
