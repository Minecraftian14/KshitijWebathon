from django.utils import timezone
from djongo import models


class User(models.Model):
    name = models.CharField(primary_key=True, max_length=40)
    password = models.CharField(max_length=69)
    mail = models.CharField(max_length=69)

    objects = models.DjongoManager()

    def __str__(self):
        return f'user;{self.name};{self.mail}'


class Competition(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    max_members = models.IntegerField(default=0)

    objects = models.DjongoManager()

    @staticmethod
    def delete_old_competitions():
        Competition.objects.filter(date__lt=timezone.now()).delete()

    def __str__(self):
        return f'competition;{self.name};{self.description};{self.date};{self.venue};{self.max_members}'

    def short_table(self, append=None):
        res = {
            'id': self.pk, 'name': self.name, 'description': self.description, 'date': self.date, 'venue': self.venue,
            'max_members': self.max_members
        }
        if append is not None:
            res.update(append)
        return res


class TeamDetails(models.Model):
    name = models.CharField(max_length=40)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    vacant_spaces = models.IntegerField(default=0)
    members = models.ArrayReferenceField(to=User, on_delete=models.CASCADE)

    objects = models.DjongoManager()

    def __str__(self):
        return f'team;{self.name};{self.competition};{self.vacant_spaces};{self.members}'

    def short_table(self, append=None):
        res = {
            'id': self.pk,
            'name': self.name,
            'vacant_spaces': self.vacant_spaces,
        }
        if append is not None:
            res.update(append)
        return res

    def long_table(self):
        return {
            'id': self.pk,
            'name': self.name,
            'c_name': self.competition.name,
            'date': self.competition.date,
            'venue': self.competition.venue,
            'vacant_spaces': self.vacant_spaces
        }


class Request(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamDetails, on_delete=models.CASCADE)
    request_message = models.CharField(max_length=100)

    objects = models.DjongoManager()

    def table(self):
        return {
            'id': self.pk,
            'u_name': self.author.name,
            'request_message': self.request_message
        }
