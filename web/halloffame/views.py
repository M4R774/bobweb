from django.shortcuts import render
from halloffame.models import *

# Create your views here.
from django.http import HttpResponse


def index(request):
    # company = get_object_or_404(Company, pk=company_id)
    chats = Chat.objects.all()
    return render(request, 'main.html', {'chats': chats})