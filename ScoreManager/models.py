from django.db import models
from polymorphic.models import PolymorphicModel


class Team(models.Model):
    title = models.CharField(max_length=50)
    mentor = models.IntegerField()
    score = models.IntegerField()


class Person(models.Model):
    first = models.CharField(max_length=50)
    second = models.CharField(max_length=50)
    middle = models.CharField(max_length=50, blank=True)
    score = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.second + " " + self.first + " " + self.middle


# class Event(models.Model):
class Event(PolymorphicModel):
    title = models.CharField(max_length=50)
    max_point = models.IntegerField(null=True)
    type = models.IntegerField(null=True)
    attendance = models.ManyToManyField(Person, through='ScoreLog')
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    #
    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.title


class Quiz(Event):
    test = models.IntegerField(default=0)


class Lecture(Event):
    subject = models.CharField(max_length=50, null=True)


class ScoreLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.event) + " \\ " + str(self.person)


class Voting(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.event) + " > " + self.title

class Choice(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
