from rest_framework import serializers
from api.models import MainUser,Token,Estelam,Status,Staff


class EstelamLatestStatusSerializer(serializers.ModelSerializer):
    staffname = serializers.SerializerMethodField('get_staffname')
    staffcode = serializers.SerializerMethodField('get_staffcode')
    status = serializers.SerializerMethodField('get_status')
    statusissuedat = serializers.SerializerMethodField('get_statusissuedat')

    def get_staffname(self,user):
        return self.context['staffname']

    def get_staffcode(self,user):
        return self.context['staffcode']

    def get_status(self,user):
        return self.context['status']

    def get_statusissuedat(self,user):
        return self.context['statusissuedat']


    class Meta:
        model = Estelam
        fields = ('issuedat','description','trackingnumber','staffname','staffcode','status','statusissuedat')


class StatusSerializer(serializers.ModelSerializer):
    staffname = serializers.SerializerMethodField('get_staffname')
    staffcode = serializers.SerializerMethodField('get_staffcode')

    def get_staffname(self, user):
        return self.context['staffname']

    def get_staffcode(self, user):
        return self.context['staffcode']


    class Meta:
        model = Status
        fields = ('issuedat', 'description', 'file', 'staffname', 'staffcode')


class EstelamSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, user):
        return self.context['staffname']


    class Meta:
        model = Estelam
        fields = ('issuedat', 'description', 'trackingnumber', 'status')


class EstelamUserGetSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')
    userphone = serializers.SerializerMethodField('get_userphone')

    def get_status(self, user):
        return self.context['username']

    def get_status(self, user):
        return self.context['userphone']


    class Meta:
        model = Estelam
        fields = ('issuedat', 'description', 'trackingnumber', 'username', 'userphone')