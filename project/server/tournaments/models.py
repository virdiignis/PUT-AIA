import itertools
import math

from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tournaments")
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    place = models.TextField()
    max_participants = models.IntegerField()
    application_deadline = models.DateTimeField()

    class Meta:
        unique_together = ("name", "time", "place")

    def __str__(self):
        return self.name

    def create_encounters(self):
        if self.encounters.count() == 0:
            participants_ids = self.participants.order_by("ranking").values_list("id", flat=True)

            Encounter.objects.bulk_create(
                Encounter(
                    participant1_id=p1,
                    participant2_id=p2,
                    tournament=self
                ) for p1, p2 in itertools.combinations(participants_ids, 2)
            )


class Sponsor(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="sponsors")
    logo = models.ImageField(upload_to="logos")
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("tournament", "name")


class Participation(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    license = models.CharField(max_length=16)
    ranking = models.IntegerField()

    @property
    def points(self):
        return self.wins1.count()

    class Meta:
        unique_together = (("tournament", "user"), ("tournament", "license"), ("tournament", "ranking"))

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Encounter(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="encounters")
    participant1 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='encounters1')
    participant2 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='encounters2')
    winner1 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='wins1', null=True, blank=True)
    winner2 = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='wins2', null=True, blank=True)
    agreed = models.BooleanField(default=False)

    def __str__(self):
        p1 = self.participant1
        p2 = self.participant2
        return f"{str(p1)} vs. {str(p2)}"

    def set_winner(self, user, winner):
        winner = self.participant1 if winner == 1 else self.participant2 if winner == 2 else None
        result = True

        if user == self.participant1.user:
            self.winner1 = winner
            if self.winner1 == self.winner2:
                self.agreed = True
            elif self.winner2 is not None:
                self.winner1 = None
                self.winner2 = None
                result = False
        elif user == self.participant2.user:
            self.winner2 = winner
            if self.winner1 == self.winner2:
                self.agreed = True
            elif self.winner1 is not None:
                self.winner1 = None
                self.winner2 = None
                result = False
        self.save()
        return result

    def whoami(self, user):
        return 1 if user == self.participant1.user else 2 if user == self.participant2.user else None
