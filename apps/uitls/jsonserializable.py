import uuid
from datetime import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            #return obj.__str__()
            return "{}-{}-{} {}:{}:{}".format(obj.year, obj.month, obj.day,obj.hour,obj.minute,obj.second)
        elif isinstance(obj,  uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
