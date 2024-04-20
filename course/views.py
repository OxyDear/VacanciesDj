from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


# Create your views here.
def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city.lower()
        if language:
            _filter['language__slug'] = language.lower()

        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'course/home.html', {'object_list': qs, 'form': form})
