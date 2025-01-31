from .models import Ville
from .models import Machine
from .models import Usine
from .models import Siege_social
from .models import Ressource
from .models import Quantite_Ressource
from .models import Etape
from .models import Produit
from .models import Stock
from django.views.generic import DetailView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class VilleDetailView(DetailView):
    model = Ville

    def get_object(self):
        nom = self.kwargs.get("nom")
        return get_object_or_404(Ville, nom=nom)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class VilleDetailViewID(DetailView):
    model = Ville

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
        return JsonResponse(self.object.json())


class Siege_socialDetailViewID(DetailView):
    model = Siege_social

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class RessourceDetailViewID(DetailView):
    model = Ressource

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class Quantite_RessourceDetailViewID(DetailView):
    model = Quantite_Ressource

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json_extended())


class EtapeDetailViewID(DetailView):
    model = Etape

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class ProduitDetailViewID(DetailView):
    model = Produit

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class StockDetailViewID(DetailView):
    model = Stock

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


####################################################


class VilleDetailAPIView(APIView):
    def get(self, request, pk):
        ville = get_object_or_404(Ville, pk=pk)
        return JsonResponse(ville.json_extended(), safe=False)


class MachineDetailAPIView(APIView):
    def get(self, request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        return JsonResponse(machine.json_extended(), safe=False)


class UsineDetailAPIView(APIView):
    def get(self, request, pk):
        usine = get_object_or_404(Usine, pk=pk)
        return JsonResponse(usine.json_extended(), safe=False)


class SiegeSocialDetailAPIView(APIView):
    def get(self, request, pk):
        siege_social = get_object_or_404(Siege_social, pk=pk)
        return JsonResponse(siege_social.json_extended(), safe=False)


class RessourceDetailAPIView(APIView):
    def get(self, request, pk):
        ressource = get_object_or_404(Ressource, pk=pk)
        return JsonResponse(ressource.json_extended(), safe=False)


class QuantiteRessourceDetailAPIView(APIView):
    def get(self, request, pk):
        quantite_ressource = get_object_or_404(Quantite_Ressource, pk=pk)
        return JsonResponse(quantite_ressource.json_extended(), safe=False)


class EtapeDetailAPIView(APIView):
    def get(self, request, pk):
        etape = get_object_or_404(Etape, pk=pk)
        return JsonResponse(etape.json_extended(), safe=False)


class ProduitDetailAPIView(APIView):
    def get(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        return JsonResponse(produit.json_extended(), safe=False)


class StockDetailAPIView(APIView):
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return JsonResponse(stock.json_extended(), safe=False)
