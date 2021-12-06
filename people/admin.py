from django.contrib import admin
from django.db import models
from django.forms import Textarea

from people.models import Person, PersonInfoPoint


class PersonInfoPointInline(admin.TabularInline):
    model = PersonInfoPoint
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (
        PersonInfoPointInline,
    )
    list_display = ('__str__', 'target_dossier_url')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }
