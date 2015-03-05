from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


class UserSerializer(ModelSerializer):
    id = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', )

    def get_id(self, obj):
        return obj.pk
