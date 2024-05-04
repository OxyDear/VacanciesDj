import json
import os, sys
import codecs
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "djangoProject.settings"
import django
django.setup()

from course.models import City, Vacancy, Language
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()


with codecs.open('jobs.json', 'r', 'utf-8') as file:
    src = json.loads(file.read())

for job in src:
    v = Vacancy(url=job['url'],
                title=job['title'],
                company=job['company'],
                description=job['content'][:460]+'...',
                city=city,
                language=language)
    try:
        v.save()
    except DatabaseError:
        pass
