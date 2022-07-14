from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ScoreManager.models import Event, Person, ScoreLog
# from ScoreManager.urls import PersonSerializer

import csv
from io import StringIO

"""
Тут написаны методы и классы которые отвечает за обработку и отправления нужных данных при определенных запросах 
"""


class PersonSerializer(
    serializers.ModelSerializer):

    """
    Класс наследник ModelSerializer, отвечает за оформление JSON объекты из объекта
    класса Person
    """

    class Meta:
        model = Person
        fields = ['first', 'middle', 'second', 'score', 'team']

    def create(self, validated_data):
        Person.objects.create(**validated_data)

    # def update(self, person, validated_data):


class UserSerializer(serializers.ModelSerializer):
    """
    Класс наследник ModelSerializer, отвечает за оформление JSON объекты из объекта
    класса User
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


#
# class TestView(APIView):
#     def get(self, request):
#         return Response({"data": request.headers})


class PersonView(APIView):

    """
    Класс наследник APIView, отвечает за операции связаны с моделем Person
    """

    parser_classes = [JSONParser]

    def get(self, request):
        # Метод GET возвращает данные об объекте Person с соответственным id в запросе

        person = Person.objects.get(id=request.data['id'])
        serializer = PersonSerializer(person)
        data = serializer.data
        return Response({"data": data})


class PersonScoreView(APIView):
    """
    Класс наследник APIView, отвечает за рейтинг и баллы
    """

    parser_classes = [JSONParser]

    def get(self, request):
        # метод запроса количество баллов участника по id
        person = Person.objects.get(id=request.data['id'])
        score = person.score
        return Response({"data": {
            "score": score
        }})

    def post(self, request):
        # метод добавления баллов участнику по id
        person = Person.objects.get(id=request.data['id'])
        score = request.data['score']
        person.score += score
        person.save()

        return Response({
            "msg": f"added {score} points to {person.first} {person.second}",
            "data": {
                "person": f"{person.first} {person.second}",
                "score": person.score
            }
        })


class EventAttendence(APIView):

    """
    Класс наследник APIView, отвечает за поосещаемость
    """

    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request):
        # запрос список участников пристусвующих на мероприятии по id
        event = Event.objects.get(id=request.data['id'])
        people = event.attendance.all()
        serializer = PersonSerializer(people, many=True)

        return Response({'attendance': serializer.data})

    def post(self, request, format=None):
        # добавить участника в список поосещаемости мероприятия
        event = Event.objects.get(title=request.data['event'])
        people = []

        for id in request.data['person_id']:
            person = Person.objects.get(id=id)
            people.append(person)
            event.attendance.add(person)

        event.save()
        serializer = PersonSerializer(people, many=True)
        return Response({'added': serializer.data})

    def put(self, request, format=None):
        # загрузка файла csv с данными (id участника и id мероприятия), который система обработает
        # и за тем  отмечает поосещаемость

        file_obj = request.data['file']
        event = Event.objects.get(id=request.data['event'])
        if file_obj.content_type == "text/csv":
            file = file_obj.read().decode('utf-8')
            csv_data = csv.DictReader(StringIO(file), delimiter=',')
            count = 0
            for row in csv_data:
                log = ScoreLog(person_id=row['person'], event_id=request.data['event'])
                count += 1
                log.save()
            return Response({"event": str(event), "added": count})

        return Response(status=400)


class EventScoreController(APIView):
    """
    Класс наследник APIView, отвечает за рейтинг на мероприятиях
    """
    parser_classes = [JSONParser]

    def post(self, request):
        # метод добавления баллов соответственных рейтингу на мероприятии

        event = Event.objects.get(title=request.data['event'])
        person = Person.objects.get(id=request.data['person_id'])

        rating = int(request.data['rating'])

        if 0 <= rating <= 10:
            rating /= 10
            added = event.max_point * rating
            person.score += added
            person.save()
            return Response({'status': f'added {added}'})

        return Response({'error': 'rating should be between 0 and 10'})


class TokenTester(APIView):# можешь не смотреть на это
    parser_classes = [JSONParser]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


def index(request):
    return render(request, 'ScoreManager/index.html')
