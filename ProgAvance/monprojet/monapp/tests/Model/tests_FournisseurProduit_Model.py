from django.test import TestCase
from monapp.models import Product, Fournisseur, FournisseurProduit

class FournisseurProduitModelTest(TestCase):
    def setUp(self):
        # Créer un produit et un fournisseur à utiliser dans les tests
        self.product = Product.objects.create(name="iPhone", code="IP12", status=1)
        self.fournisseur = Fournisseur.objects.create(nom="Apple", adresse="USA")
        self.fournisseur_produit = FournisseurProduit.objects.create(
            produit=self.product, 
            fournisseur=self.fournisseur, 
            price_ttc=999.99, 
            stock=100
        )

    def test_fournisseur_produit_creation(self):
        """
        Tester si un FournisseurProduit est bien créé
        """
        self.assertEqual(self.fournisseur_produit.produit.name, "iPhone")
        self.assertEqual(self.fournisseur_produit.fournisseur.nom, "Apple")
        self.assertEqual(self.fournisseur_produit.price_ttc, 999.99)
        self.assertEqual(self.fournisseur_produit.stock, 100)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle FournisseurProduit
        """
        self.assertEqual(str(self.fournisseur_produit), "iPhone par Apple")

    def test_update_fournisseur_produit(self):
        """
        Tester la mise à jour d'un FournisseurProduit
        """
        self.fournisseur_produit.stock = 150
        self.fournisseur_produit.save()
        # Récupérer l'objet mis à jour
        updated_fournisseur_produit = FournisseurProduit.objects.get(id=self.fournisseur_produit.id)
        self.assertEqual(updated_fournisseur_produit.stock, 150)

    def test_delete_fournisseur_produit(self):
        """
        Tester la suppression d'un FournisseurProduit
        """
        self.fournisseur_produit.delete()
        self.assertEqual(FournisseurProduit.objects.count(), 0)
