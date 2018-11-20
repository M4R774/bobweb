from django.shortcuts import render
from halloffame.models import *

# Create your views here.
from django.http import HttpResponse


def index(request):
    # TODO: Make this id to come from the settings.json
    chat = Chat.objects.get(id='-1001088846469')
    return render(request, 'main.html', {'chat': chat})