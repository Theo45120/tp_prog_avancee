from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Product, Fournisseur

class ProductCreateViewTest(TestCase):
    def setUp(self):
        # Créer un super-utilisateur pour les tests
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        # Créer un fournisseur pour l'associer au produit
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/new_product.html')

    def test_create_view_post_valid(self):
        """
        Tester que la vue de création crée un nouvel objet lorsque les données sont valides
        """
        data = {
            'name': 'Produit Test',
            'code': 'PT001',
            'status': 1,
            'fournisseurs': [self.fournisseur.id]
        }
        response = self.client.post(reverse('product-add'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un produit a été créé
        self.assertEqual(Product.objects.count(), 1)
        # Vérifie les détails du produit créé
        self.assertEqual(Product.objects.first().name, 'Produit Test')

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données
        """
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/detail_product.html')
        self.assertContains(response, 'Produit Test')
        self.assertContains(response, 'PT001')

class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)

    def test_update_view_get(self):
        """
        Tester que la vue de mise à jour s'affiche correctement
        """
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/update_product.html')

    def test_update_view_post_valid(self):
        """
        Tester que la vue met à jour l'objet lorsque les données sont valides
        """
        data = {
            'name': 'Produit Modifié',
            'code': 'PT001M',
            'status': 2,
            'fournisseurs': [self.fournisseur.id]
        }
        response = self.client.post(reverse('product-update', args=[self.product.id]), data)
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.product.refresh_from_db()
        # Vérifier la mise à jour
        self.assertEqual(self.product.name, 'Produit Modifié')
        self.assertEqual(self.product.status, 2)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)

    def test_delete_view_get(self):
        """
        Tester que la vue de suppression s'affiche correctement
        """
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/delete_product.html')

    def test_delete_view_post(self):
        """
        Tester que l'objet est supprimé lorsque le formulaire de suppression est soumis
        """
        response = self.client.post(reverse('product-delete', args=[self.product.id]))
        # Redirection après suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet est supprimé
        self.assertEqual(Product.objects.count(), 0)

class ProductListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        self.client.login(username='adminuser', password='secret')
        self.product = Product.objects.create(name="Produit Test", code="PT001", status=1)

    def test_list_view(self):
        """
        Tester que la vue de liste renvoie le bon template et affiche les données des produits
        """
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monapp/list_products.html')
        # Vérifier que le produit est listé
        self.assertContains(response, 'Produit Test')
