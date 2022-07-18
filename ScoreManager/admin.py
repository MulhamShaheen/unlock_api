from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import *

admin.site.register(Team)



class EventChildAdmin(PolymorphicChildModelAdmin):
    base_model = Event


@admin.register(Quiz)
class ModelBAdmin(EventChildAdmin):
    base_model = Quiz  # Explicitly set


@admin.register(Lecture)
class ModelBAdmin(EventChildAdmin):
    base_model = Lecture  # Explicitly set


@admin.register(Event)
class ModelAParentAdmin(PolymorphicParentModelAdmin):
    base_model = Event  # Optional, explicitly set here.
    child_models = (Quiz, Lecture)
    list_filter = (PolymorphicChildModelFilter, 'date')  # This is optional.
    list_display = ['id', 'title', 'max_point']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['id', 'first', 'second', 'score']
    list_editable = ['score']
    list_filter = ('event',)


@admin.register(ScoreLog)
class ScoreLogAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['event', 'person', 'rating']
    list_editable = ['rating']
    list_filter = ('event',)

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    model = Voting
    list_display = ['title', 'event']
    # list_editable = ['title']
    list_filter = ('event',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    model = Choice
    list_display = ['title', 'count', 'voting']
    list_editable = ['count']
    list_filter = ('voting',)
