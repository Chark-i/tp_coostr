from django.views.generic import ListView
from .models import Ville


class VilleListView(ListView):
    model = Ville
