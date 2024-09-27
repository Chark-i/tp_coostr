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
from high_level.views import MachineDetailView
from high_level.views import MachineDetailViewID
from high_level.views import UsineDetailViewID

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ville/<str:nom>/", VilleDetailView.as_view(), name="ville-detail"),
    path("machine/<int:pk>/", MachineDetailViewID.as_view(), name="machine-detail"),
    path("usine/<int:pk>/", UsineDetailViewID.as_view(), name="usine-detail"),
    path("machine/<str:nom>/", MachineDetailView.as_view(), name="machine-detail"),
]

# acceder a une ville:
# http://localhost:8000/ville/'nom_ville'/
