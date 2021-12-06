import random
from typing import Callable

from django.core.management.base import BaseCommand

from people.models import Person


def person_filter(gifter: Person) -> Callable[[Person], bool]:
    def _gifted_filter(gifted: Person) -> bool:
        return all((
            gifter.group != gifted.group,  # exclude group
            not gifted.has_present,  # exclude already with presents
        ))

    return _gifted_filter


def shuffle_presents(persons: set[Person]):
    persons_ = list(persons)
    random.shuffle(persons_)
    for person in persons_:
        filter_ = person_filter(person)
        gifted = random.choice(list(filter(filter_, persons)))

        person.present_to = gifted

        person.save()


def validate_shuffle(persons: set[Person]):
    for person in persons:
        assert person.has_present, f'{person} wihtout present!'
        assert person.present_to is not None, f'{person} without gifted person!'
        assert person.group != person.present_to.group, \
            f'Present from {person} to {person.present_to} in the same group!'


class Command(BaseCommand):
    help = 'Shuffles all gifters'

    def handle(self, *args, **options):
        Person.objects.update(present_to=None)
        shuffle_presents(set(Person.objects.all()))
        validate_shuffle(set(Person.objects.all()))

        for person in Person.objects.all():
            print(f'{person}: {person.target_dossier_url}')
