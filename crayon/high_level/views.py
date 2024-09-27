from .models import Ville
from .models import Machine
from .models import Usine
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class VilleDetailView(DetailView):
    model = Ville

    def get_object(self):
        nom = self.kwargs.get("nom")
        return get_object_or_404(Machine, nom=nom)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class MachineDetailView(DetailView):
    model = Machine

    def get_object(self):
        nom = self.kwargs.get("nom")
        return get_object_or_404(Machine, nom=nom)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class MachineDetailViewID(DetailView):
    model = Machine

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class UsineDetailViewID(DetailView):
    model = Usine

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json_extended())
