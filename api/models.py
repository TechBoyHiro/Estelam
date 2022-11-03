from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class MainUser(models.Model):
    name = models.TextField(blank=True,null=True)
    email = models.TextField(blank=True,null=True)
    phone = models.CharField(max_length=11)
    address = models.TextField(blank=True,null=True)
    job = models.TextField(blank=True,null=True)
    age = models.IntegerField(default=0)
    isauthenticated = models.BooleanField(default=0)
    datejoin = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name + ' ** ' + self.phone


class Token(models.Model):
    user = models.ForeignKey(MainUser,on_delete=models.RESTRICT)
    token = models.CharField(max_length=64)


class Staff(models.Model):
    name = models.TextField()
    staffcode = models.IntegerField(default=0)
    password = models.TextField(max_length=10,blank=True,null=True)
    section = models.TextField(blank=True, null=True)
    load = models.IntegerField(default=0) # TODO: The number of estelam assigned to this staff

    def __str__(self):
        return self.name + ' ** ' + str(self.staffcode) + ' ** ' + self.section + ' ** ' + str(self.load)


class Estelam(models.Model):
    user = models.ForeignKey(MainUser,on_delete=models.RESTRICT)
    staff = models.ForeignKey(Staff,on_delete=models.RESTRICT)
    issuedat = models.DateTimeField(default=datetime.now())
    description = models.TextField(blank=True,null=True)
    trackingnumber = models.CharField(max_length=7,blank=True,null=True)

    def __str__(self):
        return self.user.name + ' ** ' + str(self.issuedat)


class EstelamFile(models.Model):
    estelam = models.ForeignKey(Estelam,on_delete=models.CASCADE)
    file = models.FileField(upload_to='estelamfiles')

    def __str__(self):
        return self.estelam.trackingnumber


class Status(models.Model):
    estelam = models.ForeignKey(Estelam,on_delete=models.RESTRICT)
    staff = models.ForeignKey(Staff,on_delete=models.RESTRICT)
    description = models.TextField()
    issuedat = models.DateTimeField(default=datetime.now())
    file = models.FileField(upload_to='statusfiles',blank=True,null=True)

    def __str__(self):
        return 'estelam : ' + str(self.estelam.trackingnumber) + ' ** ' + self.description


class Content(models.Model):
    description = models.TextField()
    file = models.FileField(upload_to='contentfiles',blank=True,null=True)


class SMS(models.Model):
    sms = models.CharField(max_length=4)
    phone = models.CharField(max_length=11)
    issued = models.DateTimeField(default=datetime.now())
    valid = models.DateTimeField(blank=True,null=True)