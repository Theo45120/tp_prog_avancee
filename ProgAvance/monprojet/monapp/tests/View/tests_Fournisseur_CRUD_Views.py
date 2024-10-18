from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Fournisseur, Product, FournisseurProduit


class FournisseurCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')

    def test_create_view_post_valid(self):
        """
        Tester que la vue de création crée un nouveau fournisseur lorsque les données sont valides
        """
        data = {
            'nom': 'Fournisseur Test',
            'adresse': '123 Rue Test'
        }
        response = self.client.post(reverse('fournisseur-add'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertEqual(Fournisseur.objects.count(), 1)
        self.assertEqual(Fournisseur.objects.first().nom, 'Fournisseur Test')


class FournisseurDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données
        """
        response = self.client.get(reverse('fournisseur-detail', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/detail_fournisseur.html')
        self.assertContains(response, 'Fournisseur Test')


class FournisseurUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)
        FournisseurProduit.objects.create(fournisseur=self.fournisseur, produit=self.product, price_ttc=100, stock=50)

    def test_update_view_get(self):
        """
        Tester que la vue de mise à jour s'affiche correctement
        """
        response = self.client.get(reverse('fournisseur-update', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/update_fournisseur.html')

    def test_update_view_post_valid(self):
        """
        Tester que la vue met à jour un fournisseur lorsque les données sont valides
        """
        data = {
            'nom': 'Fournisseur Modifié',
            'adresse': '123 Rue Modifiée'
        }
        response = self.client.post(reverse('fournisseur-update', args=[self.fournisseur.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirection après mise à jour
        self.fournisseur.refresh_from_db()
        self.assertEqual(self.fournisseur.nom, 'Fournisseur Modifié')


class FournisseurDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")

    def test_delete_view_post(self):
        """
        Tester que le fournisseur est supprimé lorsque le formulaire de suppression est soumis
        """
        response = self.client.post(reverse('fournisseur-delete', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertEqual(Fournisseur.objects.count(), 0)


class FournisseurListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")

    def test_list_view(self):
        """
        Tester que la vue de liste renvoie le bon template et affiche les données des fournisseurs
        """
        response = self.client.get(reverse('fournisseur-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/list_fournisseurs.html')
        self.assertContains(response, 'Fournisseur Test')

    def test_search_fournisseur(self):
        """
        Tester que la recherche fonctionne correctement dans la vue de liste
        """
        response = self.client.get(reverse('fournisseur-list'), {'search': 'Fournisseur Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fournisseur Test')
        # Tester qu'une recherche qui ne correspond pas renvoie une liste vide
        response = self.client.get(reverse('fournisseur-list'), {'search': 'Non Existant'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Fournisseur Test')
