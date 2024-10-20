from django.test import TestCase
from monapp.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        # Créer un produit à utiliser dans les tests
        self.product = Product.objects.create(name="iPhone", code="IP12", status=1)

    def test_product_creation(self):
        """
        Tester si un Product est bien créé
        """
        self.assertEqual(self.product.name, "iPhone")
        self.assertEqual(self.product.code, "IP12")
        self.assertEqual(self.product.status, 1)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Product
        """
        self.assertEqual(str(self.product), "iPhone IP12")

    def test_update_product(self):
        """
        Tester la mise à jour d'un Product
        """
        self.product.name = "iPhone 12 Pro"
        self.product.save()
        # Récupérer l'objet mis à jour
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, "iPhone 12 Pro")

    def test_delete_product(self):
        """
        Tester la suppression d'un Product
        """
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)
