import mongoengine


class Player(mongoengine.Document):
    chat_id = mongoengine.LongField(required=True, unique=True, primary_key=True)
    name = mongoengine.StringField(required=True, max_length=200)
    active_game = mongoengine.StringField(null=True)
