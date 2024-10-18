from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from monapp.models import Product, Fournisseur, Commande, FournisseurProduit

class CommandeTestUrlResponses(TestCase):

    def setUp(self):
        # Créer un utilisateur administrateur pour les tests
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')

        # Créer un fournisseur, un produit et lier un FournisseurProduit
        self.fournisseur = Fournisseur.objects.create(nom="Test Fournisseur", adresse="123 Rue Test")
        self.produit = Product.objects.create(name="Test Produit", code="TP001", status=1)
        self.fournisseur_produit = FournisseurProduit.objects.create(produit=self.produit, fournisseur=self.fournisseur, price_ttc=100, stock=10)

        # Créer une commande
        self.commande = Commande.objects.create(produit=self.produit, fournisseur=self.fournisseur, quantite=5, statut='en_preparation')

    def test_avancer_commande_status_code(self):
        """
        Tester que l'URL pour avancer une commande renvoie un statut 302 (redirection) car la commande est avancée
        """
        response = self.client.get(reverse('avancer-commande', args=[self.commande.id]))
        self.assertEqual(response.status_code, 302)  # Il s'attend à une redirection après l'avancement de la commande

    def test_commande_detail_status_code(self):
        """
        Tester que l'URL des détails renvoie un statut 200 pour un ID valide
        """
        url = reverse('commande-detail', args=[self.commande.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Produit')  # Vérifier que le produit est affiché dans la page

    def test_commande_detail_status_code_invalid_id(self):
        """
        Tester que l'URL des détails renvoie un statut 404 pour un ID invalide
        """
        url = reverse('commande-detail', args=[9999])  # ID non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
