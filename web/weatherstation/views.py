from django.shortcuts import render
from weatherstation.models import *

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'chart.html')


def chart_data(request):
    # Collect the measurement data from the db
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('embarked')) \
        .order_by('embarked')

    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)