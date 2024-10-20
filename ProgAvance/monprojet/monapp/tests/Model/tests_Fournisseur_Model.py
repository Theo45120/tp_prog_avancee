from django.test import TestCase
from monapp.models import Fournisseur

class FournisseurModelTest(TestCase):
    def setUp(self):
        # Créer un fournisseur à utiliser dans les tests
        self.fournisseur = Fournisseur.objects.create(nom="Apple Inc.", adresse="1 Infinite Loop, Cupertino, CA")

    def test_fournisseur_creation(self):
        """
        Tester si un Fournisseur est bien créé
        """
        self.assertEqual(self.fournisseur.nom, "Apple Inc.")
        self.assertEqual(self.fournisseur.adresse, "1 Infinite Loop, Cupertino, CA")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Fournisseur
        """
        self.assertEqual(str(self.fournisseur), "Apple Inc.")

    def test_update_fournisseur(self):
        """
        Tester la mise à jour d'un Fournisseur
        """
        self.fournisseur.nom = "Apple Corporation"
        self.fournisseur.save()
        # Récupérer l'objet mis à jour
        updated_fournisseur = Fournisseur.objects.get(id=self.fournisseur.id)
        self.assertEqual(updated_fournisseur.nom, "Apple Corporation")

    def test_delete_fournisseur(self):
        """
        Tester la suppression d'un Fournisseur
        """
        self.fournisseur.delete()
        self.assertEqual(Fournisseur.objects.count(), 0)
