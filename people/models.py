import random

from django.db import models
from django.conf import settings

from base.models import UUIDModel


class Person(UUIDModel):
    name = models.TextField()
    photo = models.ImageField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    pin = models.CharField(max_length=4, null=True, blank=True)
    group = models.IntegerField(null=True, blank=True)
    present_to = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        related_name="present_from",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.group})"

    @property
    def number(self) -> int:
        random.seed(str(self.id))  # type: ignore
        return random.randint(100, 999)

    @property
    def has_present(self) -> bool:
        try:
            return bool(self.present_from)  # type: ignore
        except Person.DoesNotExist:
            return False

    @property
    def target_dossier_url(self):
        if self.present_to:
            return f"{settings.SITE_URL}dossier/{self.present_to.id}/"
        return "-"

    @property
    def birth_year(self):
        return self.birth_date.year if self.birth_date else None


class PersonInfoPoint(UUIDModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="info_points")
    heading = models.TextField()
    info = models.TextField()
