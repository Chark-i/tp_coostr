from django.db import models


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "code_postal": self.code_postal,
            "prix_m2": self.prix_m2,
        }

    def json_extended(self):
        return self.json()


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    n_serie = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def cost(self):
        return self.prix

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "n_serie": self.n_serie,
        }

    def json_extended(self):
        return self.json()


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {"nom": self.nom, "ville": self.ville.nom, "surface": self.surface}
        # attention dans json on ne fait pas la reference a un objet
        # ex ici ville est un objet (foreignkey) alors on utilise son identifiant
        # et pas self. ville, donc on utilise self.ville.pk

    def json_extended(self):
        return {"nom": self.nom, "ville": self.ville.json(), "surface": self.surface}

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
        return {
            "nom": self.nom,
            "ville": self.ville.nom,
            "surface": self.surface,
            "Nom_machine": [machine.nom for machine in self.machines.all()],
        }

    def json_extended(self):
        mach_total = []
        for machine in self.machines.all():
            mach = {
                "id": machine.id,
                "nom": machine.nom,
                "prix": machine.prix,
                "n_serie": machine.n_serie,
            }
            mach_total.append(mach)

        return {
            "id": self.id,
            "nom": self.nom,
            "surface": self.surface,
            "ville": self.ville.json(),
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
    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
        }

    def json_extended(self):
        return self.json()

    pass


class Quantite_Ressource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"

    def cost(self):
        prix_total = self.ressource.prix * self.quantite
        return prix_total

    def json(self):
        return {
            "id": self.id,
            "ressource": self.ressource.nom,
            "prix": self.ressource.prix,
            "quantite": self.quantite,
        }

    def json_extended(self):
        return self.json()


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    quantite_ressource = models.ForeignKey(Quantite_Ressource, on_delete=models.PROTECT)
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )

    ##null=True permet de rendre optionnel etape suivante
    ##Models.CASCADE permets de detruire,
    ##ex si on detruit le produit on detruit les etape, c'est equivalent a
    # composition forte et faible. (forte models.CASCADE ,faible models.PROTECT)

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "machine": self.machine.nom,
            "quantite_ressource": self.quantite_ressource.json(),
            "duree": self.duree,
            "etape_suivante": self.etape_suivante.nom if self.etape_suivante else None,
        }

    def json_extended(self):
        etapes = []
        current_etape = self

        while current_etape:
            etapes.append(
                {
                    "id": current_etape.id,
                    "nom": current_etape.nom,
                    "machine": current_etape.machine.json_extended(),
                    "quantite_ressource": current_etape.quantite_ressource.json(),
                    "duree": current_etape.duree,
                    "etape_suivante": current_etape.etape_suivante.nom
                    if current_etape.etape_suivante
                    else None,
                    "etape_suivante_id": current_etape.etape_suivante.id
                    if current_etape.etape_suivante
                    else None,
                }
            )
            current_etape = current_etape.etape_suivante

        return etapes


class Produit(Objet):
    premiere_etape = models.ForeignKey(Etape, null=True, on_delete=models.PROTECT)

    def json(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
            "premiere_etape": self.premiere_etape.json(),
        }

    def json_extended(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
            "premiere_etape": self.premiere_etape.json_extended(),
        }


class Stock(models.Model):
    objet = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    usine = models.ForeignKey(Usine, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.objet}"

    def json(self):
        return {
            "objet": self.objet.nom,
            "usine": self.usine.nom,
            "nombre": self.nombre,
        }

    def json_extended(self):
        return {
            "objet": self.objet.json_extended(),
            "usine": self.usine.json_extended(),
            "nombre": self.nombre,
        }
