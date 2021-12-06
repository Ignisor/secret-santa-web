from django.views.generic import DetailView

from people.models import Person


class DossierView(DetailView):
    model = Person
    template_name = 'dossier.html'
