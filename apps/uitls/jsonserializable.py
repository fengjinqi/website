import uuid
from datetime import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            #return obj.__str__()
            return "{}-{}-{} {}:{}:{}".format(obj.year, obj.month, obj.day,obj.hour,obj.minute,obj.second)
        elif isinstance(obj,  uuid.UUID):
            return str(obj)
        elif isinstance(obj, ImageFieldFile):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
