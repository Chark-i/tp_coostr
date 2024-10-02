from django.db import models


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {
            "nom": self.nom,
            "code_postal": self.code_postal,
            "prix_m2": self.prix_m2,
        }


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    n_serie = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def cost(self):
        return self.prix

    def json(self):
        return {"nom": self.nom, "prix": self.prix, "n_serie": self.n_serie}


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {"nom": self.nom, "ville": self.ville.pk, "surface": self.surface}
        # attention dans json on ne fait pas la reference a un objet
        # ex ici ville est un objet (foreignkey) alors on utilise son identifiant
        # et pas self. ville, donc on utilise self.ville.pk

    class Meta:
        abstract = True


class Siege_social(Local):
    pass


class Usine(Local):
    machines = models.ManyToManyField(Machine)

    def cost(self):
        prix_machine = 0
        prix_terrain = 0
        prix_total = 0
        prix_stock = 0
        prix_terrain = self.ville.prix_m2 * self.surface
        for machines in self.machines.all():
            prix_machine += machines.prix
        stocks = Stock.objects.filter(usine=self)
        for stock in stocks:
            prix_stock += stock.objet.prix * stock.nombre
        prix_total = prix_terrain + prix_machine + prix_stock
        return prix_total

    def json(self):
        return {"machines": self.machines}

    def json_extended(self):
        mach_total = []
        for machine in self.machines.all():
            mach = {
                "nom": machine.nom,
                "prix": machine.prix,
                "n_serie": machine.n_serie,
            }
            mach_total.append(mach)

        return {
            "nom_usine": self.nom,
            "ville": self.ville.json(),
            #'ville': self.ville.nom,
            #'code postal' : self.ville.code_postal,
            #'prix_m2' : self.ville.prix_m2,
            "surface": self.surface,
            "machines": mach_total,
        }


# for machine in self.machines.all()


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        abstract = True


class Ressource(Objet):
    pass


class Quantite_Ressource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"

    def cost(self):
        prix_total = self.ressource.prix * self.quantite
        return prix_total


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


#    def approvisionnement(self, nombre_produit):
#        if self.premiere_etape is None:
#            print("Pas d'élément dans la liste")
#            return
#        else:
#            approvisionnement = []
#            quantite_ressource = self.premiere_etape.quantite_ressource
#    for quantite_ressource in self.quantite_ressource.all():
#    quantite_ressource[i] = [
#        self.quantite_ressource.nom,
#        self.quantite_ressource.quantite * nombre_produit,
#    ]
# premiere_etape = self.etape_suivante


class Stock(models.Model):
    objet = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    usine = models.ForeignKey(Usine, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.objet}"
