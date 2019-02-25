from django.shortcuts import render
from weatherstation.models import *
from django.http import HttpResponse
import json
from django.http import JsonResponse


def index(request):
    return render(request, 'chart.html')


def chart_data(request):
    # Collect the measurement data from the db
    dataset = Measurement.objects.all()
    
    temperature_set = []
    humidity_set = []
    
    temperature_queryset = Measurement.objects.all().values_list('date', 'temperature')[240:]
    for i, measurement in enumerate(temperature_queryset): 
        temperature_set.insert(i, (measurement[0], measurement[1]))
    humidity_queryset = Measurement.objects.all().values_list('date', 'humidity')[240:]
    for i, measurement in enumerate(humidity_queryset): 
        humidity_set.insert(i, (measurement[0], measurement[1]))
    
    chart = {
        'title': {'text': 'Lämpötila ja suhteellinen kosteus'},
        'subtitle': {'text': 'Aleksi Martikainen'},
        'xAxis': {'type': 'datetime'},
        
        
        'yAxis': [
            { # Primary yAxis
                'title': {
                    'text': 'Temperature',
                },
                'labels': {
                    'format': '{value} °C',
                },
            }, 
            { # Secondary yAxis
                'title': {
                    'text': 'Relative Humidity',
                },
                'labels': {
                    'format': '{value} %',
                },
                'opposite': 'true'
            }],
        
        'series': [
        {
            'name': 'Temperature',
            'data': list(map(lambda x:(float(x[0].strftime('%s'))*1000, float(x[1])), temperature_set))
        },
        {   
            'name': 'Relative Humidity',
            'data': list(map(lambda x:(float(x[0].strftime('%s'))*1000, float(x[1])), humidity_set)),
            'yAxis': 1
        }]
    }
    return JsonResponse(chart)

    
    
    
    
    
