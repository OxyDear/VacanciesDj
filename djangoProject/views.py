from django.shortcuts import render
from datetime import datetime


def home(request):
    date = datetime.now().date()
    name = "Ivan"
    _context = {"date": date, "name": name}

    return render(request, 'base.html', _context)
