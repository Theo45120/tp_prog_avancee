from django.test import TestCase
from monapp.forms import ProductForm
from monapp.models import Product, Fournisseur

class ProductFormTest(TestCase):
    def setUp(self):
        # Créer un fournisseur pour l'associer au produit
        self.fournisseur = Fournisseur.objects.create(nom="Apple", adresse="USA")

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = ProductForm(data={
            'name': 'MacBook Pro',
            'code': 'MBP16',
            'status': 1,
            'fournisseurs': [self.fournisseur.id]  # Associer un fournisseur
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si le champ 'name' est manquant
        """
        form = ProductForm(data={
            'code': 'MBP16',
            'status': 1,
            'fournisseurs': [self.fournisseur.id]
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('name', form.errors)  # Le champ 'name' doit contenir une erreur

    def test_form_invalid_code(self):
        """
        Tester que le formulaire est invalide si le champ 'code' est manquant
        """
        form = ProductForm(data={
            'name': 'MacBook Pro',
            'status': 1,
            'fournisseurs': [self.fournisseur.id]
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('code', form.errors)  # Le champ 'code' doit contenir une erreur

    def test_form_optional_status(self):
        """
        Tester que le formulaire est valide même si le champ 'status' est omis
        """
        form = ProductForm(data={
            'name': 'MacBook Pro',
            'code': 'MBP16',
            'fournisseurs': [self.fournisseur.id]
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = ProductForm(data={
            'name': 'iPhone',
            'code': 'IP12',
            'status': 1,
            'fournisseurs': [self.fournisseur.id]
        })
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, 'iPhone')
        self.assertEqual(product.code, 'IP12')
        self.assertEqual(product.status, 1)
