from django.test import TestCase
from monapp.models import Product, Fournisseur, FournisseurProduit, Commande
from django.utils import timezone

class CommandeModelTest(TestCase):
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
        # Créer une commande à utiliser dans les tests
        self.commande = Commande.objects.create(
            produit=self.product,
            fournisseur=self.fournisseur,
            quantite=10,
            statut='en_preparation',
            date_commande=timezone.now()
        )

    def test_commande_creation(self):
        """
        Tester si une Commande est bien créée
        """
        self.assertEqual(self.commande.produit.name, "iPhone")
        self.assertEqual(self.commande.fournisseur.nom, "Apple")
        self.assertEqual(self.commande.quantite, 10)
        self.assertEqual(self.commande.statut, 'en_preparation')

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Commande
        """
        self.assertEqual(str(self.commande), f"Commande de iPhone (10) chez Apple")

    def test_update_commande_statut(self):
        """
        Tester la mise à jour du statut d'une Commande
        """
        self.commande.statut = 'recue'
        self.commande.save()
        # Récupérer l'objet mis à jour
        updated_commande = Commande.objects.get(id=self.commande.id)
        self.assertEqual(updated_commande.statut, 'recue')

    def test_commande_affecte_le_stock(self):
        """
        Tester que le stock est bien mis à jour lorsque la commande est marquée 'recue'
        """
        self.commande.statut = 'recue'
        self.commande.save()
        # Vérifier que le stock a été mis à jour dans FournisseurProduit
        self.fournisseur_produit.refresh_from_db()
        self.assertEqual(self.fournisseur_produit.stock, 110)  # Le stock doit être augmenté de 10

    def test_delete_commande(self):
        """
        Tester la suppression d'une Commande
        """
        self.commande.delete()
        self.assertEqual(Commande.objects.count(), 0)
