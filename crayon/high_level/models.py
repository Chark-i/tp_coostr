from django.db import models


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    n_serie = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        abstract = True


class Siege_social(Local):
    def __init(self):
        pass


class Usine(Local):
    machines = models.ManyToManyField(Machine)


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        abstract = True


class Ressource(Objet):
    def __init(self):
        pass


class Quantite_Ressource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    quantite_ressource = models.ForeignKey(Quantite_Ressource, on_delete=models.PROTECT)
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    ##null=True permet de rendre optionnel etape suivante
    ##Models.CASCADE permets de detruire,
    ##ex si on detruit le produit on detruit les etape, c'est equivalent a
    # composition forte et faible. (forte models.CASCADE ,faible models.PROTECT)


class Produit(Objet):
    premiere_etape = models.ForeignKey(Etape, null=True, on_delete=models.PROTECT)


class Stock(models.Model):
    objet = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.objet}"
