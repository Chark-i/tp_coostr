"""
URL configuration for crayon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from high_level.views import VilleDetailView
from high_level.views import VilleDetailViewID
from high_level.views import MachineDetailView
from high_level.views import MachineDetailViewID
from high_level.views import UsineDetailViewID
from high_level.views import Siege_socialDetailViewID
from high_level.views import RessourceDetailViewID
from high_level.views import Quantite_RessourceDetailViewID
from high_level.views import EtapeDetailViewID
from high_level.views import ProduitDetailViewID
from high_level.views import StockDetailViewID
from high_level.views import (
    VilleDetailAPIView,
    MachineDetailAPIView,
    UsineDetailAPIView,
    SiegeSocialDetailAPIView,
    RessourceDetailAPIView,
    QuantiteRessourceDetailAPIView,
    EtapeDetailAPIView,
    ProduitDetailAPIView,
    StockDetailAPIView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("ville/<int:pk>/", VilleDetailViewID.as_view(), name="ville-detail"),
    path("machine/<int:pk>/", MachineDetailViewID.as_view(), name="machine-detail"),
    path("usine/<int:pk>/", UsineDetailViewID.as_view(), name="usine-detail"),
    path("machine/<str:nom>/", MachineDetailView.as_view(), name="machine-detail"),
    path("ville/<str:nom>/", VilleDetailView.as_view(), name="ville-detail"),
    path(
        "siege_social/<int:pk>/",
        Siege_socialDetailViewID.as_view(),
        name="siege_social-detail",
    ),
    path(
        "ressource/<int:pk>/", RessourceDetailViewID.as_view(), name="ressource-detail"
    ),
    path(
        "quantite_ressource/<int:pk>/",
        Quantite_RessourceDetailViewID.as_view(),
        name="quantite_ressource-detail",
    ),
    path("etape/<int:pk>/", EtapeDetailViewID.as_view(), name="etape-detail"),
    path("produit/<int:pk>/", ProduitDetailViewID.as_view(), name="produit-detail"),
    path("stock/<int:pk>/", StockDetailViewID.as_view(), name="stock-detail"),
    ####################################################""""
    path("api/ville/<int:pk>/", VilleDetailAPIView.as_view(), name="ville-detail"),
    path(
        "api/machine/<int:pk>/", MachineDetailAPIView.as_view(), name="machine-detail"
    ),
    path("api/usine/<int:pk>/", UsineDetailAPIView.as_view(), name="usine-detail"),
    path(
        "api/siege_social/<int:pk>/",
        SiegeSocialDetailAPIView.as_view(),
        name="siege_social-detail",
    ),
    path(
        "api/ressource/<int:pk>/",
        RessourceDetailAPIView.as_view(),
        name="ressource-detail",
    ),
    path(
        "api/quantite_ressource/<int:pk>/",
        QuantiteRessourceDetailAPIView.as_view(),
        name="quantite_ressource-detail",
    ),
    path("api/etape/<int:pk>/", EtapeDetailAPIView.as_view(), name="etape-detail"),
    path(
        "api/produit/<int:pk>/", ProduitDetailAPIView.as_view(), name="produit-detail"
    ),
    path("api/stock/<int:pk>/", StockDetailAPIView.as_view(), name="stock-detail"),
    # path("", admin.site.urls),
]

# acceder a une ville:
# http://localhost:8000/ville/'nom_ville'/
