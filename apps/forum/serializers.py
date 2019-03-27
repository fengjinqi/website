from rest_framework import serializers

from apps.article.serializers import UserSerializer
from apps.forum.models import Forum_plate



class Forum_plateSerializers(serializers.ModelSerializer):
    authors = UserSerializer(read_only=True)
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Forum_plate
        fields ='__all__'




