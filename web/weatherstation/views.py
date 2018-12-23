from django.shortcuts import render
from weatherstation.models import *

import pandas
from pandas import DataFrame

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


# Create your views here.
from django.http import HttpResponse


def index(request):
    fig = Figure()
    ax = fig.add_subplot(111)
    data_df = pandas.read_csv("C:/Users/martt/OneDrive/Harrasteprojektit/bobweb/web/weatherstation/templates/measurements_log.csv")
    data_df = pandas.DataFrame(data_df)
    data_df.plot(ax=ax)
    canvas = FigureCanvas(fig)
    response = HttpResponse( content_type = 'image/png')
    canvas.print_png(response)
    return response