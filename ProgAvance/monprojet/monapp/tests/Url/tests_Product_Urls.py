from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from monapp.views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView
from django.contrib.auth.models import User
from monapp.models import Product, Fournisseur

class ProductTestUrls(SimpleTestCase):
    def test_create_view_url_is_resolved(self):
        """
        Tester que l'URL de la création de Product renvoie la bonne vue
        """
        url = reverse('product-add')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_list_view_url_is_resolved(self):
        """
        Tester que l'URL de la liste de Product renvoie la bonne vue
        """
        url = reverse('product-list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_detail_view_url_is_resolved(self):
        """
        Tester que l'URL des détails de Product renvoie la bonne vue
        """
        url = reverse('product-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_update_view_url_is_resolved(self):
        """
        Tester que l'URL de mise à jour de Product renvoie la bonne vue
        """
        url = reverse('product-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductUpdateView)


class ProductTestUrlResponses(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Créer un super-utilisateur pour les tests
        cls.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')

    def setUp(self):
        # Se connecter avec l'utilisateur admin
        self.client.login(username='adminuser', password='secret')

    def test_create_view_status_code(self):
        """
        Tester que l'URL de création renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_status_code(self):
        """
        Tester que l'URL de la liste renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

class ProductTestUrlResponsesWithParameters(TestCase):
    def setUp(self):
        # Créer un produit à utiliser pour les tests
        self.product = Product.objects.create(name="MacBook Pro", code="MBP16", status=1)
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_detail_view_status_code(self):
        """
        Tester que l'URL des détails renvoie un statut 200 pour un ID valide
        """
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_status_code_invalid_id(self):
        """
        Tester que l'URL des détails renvoie un statut 404 pour un ID invalide
        """
        url = reverse('product-detail', args=[9999])  # ID non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class ProductTestUrlRedirect(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Créer un super-utilisateur pour les tests
        cls.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')
        # Créer un fournisseur à associer au produit
        cls.fournisseur = Fournisseur.objects.create(nom="Fournisseur Test", adresse="123 Rue Test")

    def setUp(self):
        # Connexion de l'utilisateur superuser pour le test
        self.client.login(username='adminuser', password='secret')

    def test_redirect_after_creation(self):
        """
        Tester qu'après la création d'un Product, l'utilisateur est redirigé correctement
        """
        # Associer le fournisseur dans les données du formulaire
        response = self.client.post(reverse('product-add'), {
            'name': 'Nouveau Produit',
            'code': 'NP01',
            'status': 1,
            'fournisseurs': [self.fournisseur.id],  # Associer le fournisseur ici
        })

        # Imprimer les erreurs de formulaire s'il y en a
        if response.status_code == 200:
            print(response.context['form'].errors)  # Affiche les erreurs de validation du formulaire

        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)

        # Obtenir l'ID du produit nouvellement créé
        product_id = Product.objects.first().id
        # Vérifier la redirection vers la page de détail du produit
        self.assertRedirects(response, reverse('product-detail', args=[product_id]))