import rest_framework.views
from django.urls import path, include

from ScoreManager.models import Person

from rest_framework import routers, viewsets
from . import views
from ScoreManager.views import *

"""
В этом файле написаны пути и URL, какой ответ получить по какой URL 
"""
# # ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersomViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'people', PersomViewSet)


urlpatterns = [
    # тут каждый путь связан с методом или классом в файле views.py
    path('main/', views.index, name='index'),
    # path('test/', TestView.as_view(), name='test'),
    path('score/', PersonScoreView.as_view(), name='person_score_path'),
    path('participant/', PersonView.as_view(), name='person_path'),
    path('attendence/', EventAttendence.as_view(), name='attendence'),
    path('event/score/', EventScoreController.as_view(), name='score'),
    # path('upload/', FileUploadView.as_view(), name='upload'),
    path('', include(router.urls)),
]
