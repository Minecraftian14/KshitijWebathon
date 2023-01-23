from djongo import models


class User(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=69)
    mail = models.CharField(max_length=69)


class Competition(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    max_members = models.IntegerField(default=0)


class TeamDetails(models.Model):
    name = models.CharField(max_length=40)
    c_name = models.CharField(max_length=40)
    vacant_members = models.IntegerField(default=0)
    team_member_id = models.BigIntegerField(null=True)

    def table(self):
        return {
            'tname': self.name,
            'vacant_members': self.vacant_members
        }


class Request(models.Model):
    c_name = models.CharField(max_length=40)
    t_name = models.CharField(max_length=40)
    request_message = models.CharField(max_length=100)


class TeamMembers(models.Model):
    team_member_id = models.BigIntegerField(default=0)
    u_name = models.BigIntegerField(default=0)
    team_member_id_back_referenced = models.BigIntegerField(null=True)
