from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Commande, Fournisseur, Product


class CommandeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)
        self.commande = Commande.objects.create(produit=self.product, fournisseur=self.fournisseur, quantite=5, statut='en_preparation')

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données
        """
        response = self.client.get(reverse('commande-detail', args=[self.commande.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/commande_detail.html')
        self.assertContains(response, 'Produit Test')
        self.assertContains(response, 'En préparation')



class CommandeDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)
        self.commande = Commande.objects.create(produit=self.product, fournisseur=self.fournisseur, quantite=5, statut='en_preparation')

    def test_delete_view_post(self):
        """
        Tester que la commande est supprimée lorsque le formulaire de suppression est soumis
        """
        response = self.client.post(reverse('commande-delete', args=[self.commande.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertEqual(Commande.objects.count(), 0)  # La commande doit être supprimée

class CommandeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)
        self.commande = Commande.objects.create(produit=self.product, fournisseur=self.fournisseur, quantite=5, statut='en_preparation')

    def test_list_view(self):
        """
        Tester que la vue de liste renvoie le bon template et affiche les données des commandes
        """
        response = self.client.get(reverse('commande-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/list_commande.html')
        self.assertContains(response, 'Produit Test')
        self.assertContains(response, 'en_preparation')
