from django.db import models
from django.utils import timezone
from datetime import timedelta

PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)

# Create your models here.

"""
    Status : numero, libelle
"""
class Status(models.Model):
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)
          
    def __str__(self):
        return "{0} {1}".format(self.numero, self.libelle)
    

"""
Produit : nom, code, etc.
"""
class Product(models.Model):
    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=False, blank=False, unique=True)
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=1)
    date_creation = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Date création")
    fournisseurs  = models.ManyToManyField('Fournisseur', through='FournisseurProduit')

    def __str__(self):
        return "{0} {1}".format(self.name, self.code)

    # Suppression de la méthode de mise à jour du stock ici, car le stock est géré dans FournisseurProduit



"""
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
"""
class ProductItem(models.Model):
    
    class Meta:
        verbose_name = "Déclinaison Produit"

    color   = models.CharField(max_length=100)
    code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", null=True, blank=True)
       
    def __str__(self):
        return "{0} {1}".format(self.color, self.code)


class ProductAttribute(models.Model):
    """
    Attributs produit
    """
    
    class Meta:
        verbose_name = "Attribut"
        
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """
    
    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']
        
    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité", on_delete=models.CASCADE)
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)
     
    def __str__(self):
        return "{0} [{1}]".format(self.value, self.product_attribute)
    

"""
    Fournisseur : gestion des fournisseurs
"""
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()

    def __str__(self):
        return self.nom


"""
    FournisseurProduit : relation entre produit et fournisseur avec prix spécifique
"""
class FournisseurProduit(models.Model):
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    price_ttc = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    stock = models.IntegerField(default=0)  # Stock spécifique au fournisseur pour ce produit

    class Meta:
        unique_together = ('produit', 'fournisseur')

    def __str__(self):
        return f"{self.produit.name} par {self.fournisseur.nom}"

    # def mettre_a_jour_stock(self, quantite):
    #     """Met à jour le stock du produit pour ce fournisseur."""
    #     self.stock += quantite
    #     self.save()


"""
    Commande : gestion des commandes passées aux fournisseurs
"""
class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_preparation', 'En préparation'),
        ('passee', 'Passée'),
        ('recue', 'Reçue'),
    ]

    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_preparation')
    date_commande = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        Ne met à jour le stock dans FournisseurProduit que lorsque 
        le statut de la commande passe à "recue".
        """
        # Vérifier si c'est une mise à jour et non une création
        if self.pk is not None:
            ancienne_commande = Commande.objects.get(pk=self.pk)

            # Si la commande passe de 'passee' à 'recue' et n'était pas déjà reçue
            if ancienne_commande.statut != 'recue' and self.statut == 'recue':
                fournisseur_produit = FournisseurProduit.objects.get(produit=self.produit, fournisseur=self.fournisseur)
                fournisseur_produit.stock += self.quantite  # Ajouter au stock uniquement quand reçue
                fournisseur_produit.save()

        super().save(*args, **kwargs)

    def changer_statut_automatiquement(self):
        """
        Change le statut automatiquement après un délai :
        - 20 secondes pour passer de "en_preparation" à "passee"
        - 40 secondes pour passer de "passee" à "recue"
        """
        now = timezone.now()
        if self.statut == 'en_preparation' and now >= self.date_commande + timedelta(seconds=20):
            self.statut = 'passee'
        elif self.statut == 'passee' and now >= self.date_commande + timedelta(seconds=40):
            self.statut = 'recue'
        self.save()

    def __str__(self):
        return f"Commande de {self.produit.name} ({self.quantite}) chez {self.fournisseur.nom}"
