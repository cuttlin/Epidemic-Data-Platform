import mongoengine
# Create your models here.

class City(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    size = mongoengine.StringField(max_length=32)


class Overviewchina(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

    #def __init__(self):
