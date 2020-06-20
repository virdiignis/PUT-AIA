from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tournaments")
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    place = models.TextField()
    max_participants = models.IntegerField()
    application_deadline = models.DateTimeField()


class Sponsor(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="sponsors")
    logo = models.ImageField(upload_to="logos")
    name = models.CharField(max_length=255)


class Participation(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    license = models.CharField(max_length=16)
    ranking = models.IntegerField()

    class Meta:
        unique_together = (("tournament", "user"), ("tournament", "license"), ("tournament", "ranking"))


class Encounter(models.Model):
    participant1 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='encounters1')
    participant2 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='encounters2')
    winner = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='wins', null=True, blank=True)
    agreed = models.BooleanField(default=False)
