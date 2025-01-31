from django.test import TestCase
from .models import Machine
from .models import Ressource
from .models import Usine
from .models import Ville
from .models import Stock
from .models import Quantite_Ressource


class MachineModelTests(TestCase):
    def test_machine_cout(self):
        machine = Machine.objects.create(nom="scie", prix=1000, n_serie="16832")
        self.assertEqual(machine.cost(), 1000)  # Create your tests here.


class RessourceModelTests(TestCase):
    def test_ressource_cout(self):
        ressource1 = Ressource.objects.create(nom="bois", prix=1)
        qu_ressource = Quantite_Ressource.objects.create(
            ressource=ressource1, quantite=1000
        )
        self.assertEqual(qu_ressource.cost(), 1000)  # Create your tests here.


class UsineModelTests(TestCase):
    def test_usine_cout(self):
        ressource1 = Ressource.objects.create(nom="bois", prix=10)
        ressource2 = Ressource.objects.create(nom="mine", prix=15)
        ville = Ville.objects.create(nom="Labege", code_postal=31000, prix_m2=2000)
        usine = Usine.objects.create(nom="Usine Test", ville=ville, surface=50)
        machine1 = Machine.objects.create(nom="scie", prix=1000, n_serie="16832")
        machine2 = Machine.objects.create(nom="limeuse", prix=2000, n_serie="16833")
        usine.machines.add(machine1, machine2)
        Stock.objects.create(objet=ressource1, usine=usine, nombre=1000)
        Stock.objects.create(objet=ressource2, usine=usine, nombre=50)
        self.assertEqual(usine.cost(), 113750)
