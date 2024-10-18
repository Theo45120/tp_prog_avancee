from django.test import TestCase
from monapp.forms import FournisseurForm, FournisseurUpdateForm
from monapp.models import Fournisseur

class FournisseurFormTest(TestCase):
    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = FournisseurForm(data={
            'nom': 'Fournisseur Test',
            'adresse': '123 Rue Exemple, TestVille'
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si le champ 'nom' est manquant
        """
        form = FournisseurForm(data={
            'adresse': '123 Rue Exemple, TestVille'
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('nom', form.errors)  # Le champ 'nom' doit contenir une erreur

    def test_form_invalid_adresse(self):
        """
        Tester que le formulaire est invalide si le champ 'adresse' est manquant
        """
        form = FournisseurForm(data={
            'nom': 'Fournisseur Test'
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('adresse', form.errors)  # Le champ 'adresse' doit contenir une erreur

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = FournisseurForm(data={
            'nom': 'Fournisseur Test',
            'adresse': '123 Rue Exemple, TestVille'
        })
        self.assertTrue(form.is_valid())
        fournisseur = form.save()
        self.assertEqual(fournisseur.nom, 'Fournisseur Test')
        self.assertEqual(fournisseur.adresse, '123 Rue Exemple, TestVille')


class FournisseurUpdateFormTest(TestCase):
    def setUp(self):
        # Créer un fournisseur pour l'utiliser dans les tests de mise à jour
        self.fournisseur = Fournisseur.objects.create(nom="Ancien Fournisseur", adresse="456 Rue Ancienne")

    def test_form_valid_update(self):
        """
        Tester que le formulaire de mise à jour est valide avec des données correctes
        """
        form = FournisseurUpdateForm(data={
            'nom': 'Nouveau Fournisseur',
            'adresse': '789 Rue Nouvelle'
        }, instance=self.fournisseur)
        self.assertTrue(form.is_valid())
        fournisseur = form.save()
        self.assertEqual(fournisseur.nom, 'Nouveau Fournisseur')
        self.assertEqual(fournisseur.adresse, '789 Rue Nouvelle')

    def test_form_invalid_update(self):
        """
        Tester que le formulaire de mise à jour est invalide si le champ 'nom' est manquant
        """
        form = FournisseurUpdateForm(data={
            'adresse': '789 Rue Nouvelle'
        }, instance=self.fournisseur)
        self.assertFalse(form.is_valid())
        self.assertIn('nom', form.errors)
