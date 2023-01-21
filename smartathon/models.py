from django.db import models


# Create your models here.

class User(models.Model):
    uname = models.CharField(max_length=40)
    upass = models.CharField(max_length=69)
    umail = models.CharField(max_length=69)


class Competition(models.Model):
    cname = models.CharField(max_length=40)
    cid = models.BigIntegerField(default=0)
    cdesc = models.CharField(max_length=200)
    cdate = models.DateTimeField()
    cvenue = models.CharField(max_length=200)
    max_members = models.IntegerField(default=0)


class TeamDetails(models.Model):
    tname = models.CharField(max_length=40)
    cid = models.BigIntegerField(default=0)
    members = models.IntegerField(default=0)
    tfref = models.BigIntegerField(null=True)

    def table(self):
        return {
            'tname': self.tname,
            'members': self.members
        }


class TeamMembers(models.Model):
    tfref = models.BigIntegerField(default=0)
    uname = models.BigIntegerField(default=0)
    tbref = models.BigIntegerField(null=True)
