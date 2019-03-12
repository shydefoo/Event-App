class BaseSingleEntity:
    def __init__(self):
        pass

    def extract_id(self, object):
        return str(object.id)

class SingleEvent(BaseSingleEntity):
    def __init__(self, event):
        self.datetime_of_event = event.datetime_of_event.strftime('%d-%m-%y, %H%M') if event.datetime_of_event is not None else ''
        self.description = event.description
        self.title = event.title
        self.category = list(map(self.extract_category, list(event.category.all())))
        self.location = event.location
        self.id = self.extract_id(event)
        self.likes = list(map(self.extract_id, list(event.likes.all())))
        self.participants = list(map(self.extract_id, list(event.participants.all())))
        self.get_user_absolute_url = event.get_user_absolute_url()

    # def extract_id(self, object):
    #     return object.id.hex
    def extract_category(self, category):
        return category.category

class SingleComment(BaseSingleEntity):
    def __init__(self, comment):
        self.datetime = comment.datetime.strftime('%d-%m-%y, %H%M')
        self.comment = comment.comment
        self.id = self.extract_id(comment)
        self.username = comment.user.username


class SingleEventForm(SingleEvent):
    def __init__(self, event):
        super().__init__(event)

    def extract_category(self, category):
        return category.id

class SingleUser(BaseSingleEntity):
    def __init__(self, user):
        self.id = self.extract_id(user)
        self.username = user.username
