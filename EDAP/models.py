import mongoengine
# Create your models here.

class City(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    size = mongoengine.StringField(max_length=32)


class Leijitwomonth(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Leiji(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Yiqingv2(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()