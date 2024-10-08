from django.db import models
from django.utils import timezone

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

    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Date création")
    stock         = models.IntegerField(default=0)  # Stock actuel du produit
    fournisseurs  = models.ManyToManyField('Fournisseur', through='FournisseurProduit')  # Relation avec les fournisseurs

    def __str__(self):
        return "{0} {1}".format(self.name, self.code)

    def mettre_a_jour_stock(self, quantite):
        """Met à jour le stock du produit en ajoutant la quantité."""
        self.stock += quantite
        self.save()


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
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix spécifique par fournisseur

    class Meta:
        unique_together = ('produit', 'fournisseur')

    def __str__(self):
        return f"{self.produit.name} par {self.fournisseur.nom}"


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

    def __str__(self):
        return f"Commande de {self.produit.name} ({self.quantite}) chez {self.fournisseur.nom}"

    def save(self, *args, **kwargs):
        # Met à jour le stock lorsque la commande passe à l'état "reçue"
        if self.pk and self.statut == 'recue':
            self.produit.mettre_a_jour_stock(self.quantite)
        super().save(*args, **kwargs)
