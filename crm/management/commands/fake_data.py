from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from address.models import Locality, State, Country
from faker import Faker
import random

from crm import models

class Command(BaseCommand):
    def create_model(self, Model, count, fakers):
        ret = []
        for i in range(0, count):
            args = {}
            for argName,genFunc in fakers.iteritems():
                args[argName] = genFunc()
            ret.append(Model.objects.create(**args))
        return ret

    def handle(self, *args, **options):
        if not settings.DEBUG:
                raise EnvironmentError("I won't allow you to run fake_data without setting the DEBUG environment variable.")
        fake = Faker()
        states = self.create_model(models.PersonState, 7, {
            'name': fake.word
        })
        country = Country.objects.create(name=fake.country())
        state = State.objects.create(name=fake.state(), country=country)
        locality = Locality.objects.create(name=fake.city(), state=state)
        turfs = self.create_model(models.Turf, 10, {
            'name': fake.city,
            'locality': lambda: locality
        })
        people = self.create_model(models.Person, 100, {
            'name': fake.name,
            'address': fake.address,
            'email': fake.email,
            'state': lambda: random.choice(states)
        })

        for person in people:
            models.TurfMembership.objects.create(person=person,
                    turf=random.choice(turfs))
