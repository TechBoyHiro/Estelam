from rest_framework import serializers
from api.models import MainUser,Token


class UserGetSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')

    def get_token(self,user):
        return self.context['token']


    class Meta:
        model = MainUser
        fields = ('name','email','phone','address','job','age','isauthenticated','datejoin','token')