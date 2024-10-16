# from django.test import TestCase
# from monapp.forms import FournisseurForm
# from monapp.models import Fournisseur

# class FournisseurFormTest(TestCase):
    
#     def test_form_valid_data(self):
#         """
#         Tester que le formulaire est valide avec des données correctes
#         """
#         form = FournisseurForm(data={
#             'nom': 'Microsoft',
#             'adresse': 'Redmond, WA, USA'
#         })
#         self.assertTrue(form.is_valid())  # Le formulaire doit être valide

#     def test_form_invalid_nom(self):
#         """
#         Tester que le formulaire est invalide si le champ 'nom' est manquant
#         """
#         form = FournisseurForm(data={
#             'adresse': 'USA'
#         })
#         self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
#         self.assertIn('nom', form.errors)  # Le champ 'nom' doit contenir une erreur

#     def test_form_invalid_adresse(self):
#         """
#         Tester que le formulaire est invalide si le champ 'adresse' est manquant
#         """
#         form = FournisseurForm(data={
#             'nom': 'Apple'
#         })
#         self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
#         self.assertIn('adresse', form.errors)  # Le champ 'adresse' doit contenir une erreur

#     def test_form_save(self):
#         """
#         Tester que le formulaire peut être enregistré avec des données valides
#         """
#         form = FournisseurForm(data={
#             'nom': 'Apple',
#             'adresse': 'Cupertino, CA, USA'
#         })
#         self.assertTrue(form.is_valid())
#         fournisseur = form.save()
#         self.assertEqual(fournisseur.nom, 'Apple')
#         self.assertEqual(fournisseur.adresse, 'Cupertino, CA, USA')
