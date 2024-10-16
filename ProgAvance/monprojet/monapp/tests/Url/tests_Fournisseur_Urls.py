# from django.test import TestCase
# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from monapp.views import FournisseurCreateView, FournisseurListView, FournisseurDetailView, FournisseurUpdateView
# from django.contrib.auth.models import User
# from monapp.models import Fournisseur

# class FournisseurTestUrls(SimpleTestCase):
#     def test_create_view_url_is_resolved(self):
#         """
#         Tester que l'URL de la création de Fournisseur renvoie la bonne vue
#         """
#         url = reverse('fournisseur-add')
#         self.assertEqual(resolve(url).func.view_class, FournisseurCreateView)

#     def test_list_view_url_is_resolved(self):
#         """
#         Tester que l'URL de la liste de Fournisseur renvoie la bonne vue
#         """
#         url = reverse('fournisseur-list')
#         self.assertEqual(resolve(url).func.view_class, FournisseurListView)

#     def test_detail_view_url_is_resolved(self):
#         """
#         Tester que l'URL des détails de Fournisseur renvoie la bonne vue
#         """
#         url = reverse('fournisseur-detail', args=[1])
#         self.assertEqual(resolve(url).func.view_class, FournisseurDetailView)

#     def test_update_view_url_is_resolved(self):
#         """
#         Tester que l'URL de mise à jour de Fournisseur renvoie la bonne vue
#         """
#         url = reverse('fournisseur-update', args=[1])
#         self.assertEqual(resolve(url).func.view_class, FournisseurUpdateView)


# class FournisseurTestUrlResponses(TestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         # Créer un super-utilisateur pour les tests
#         cls.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')

#     def setUp(self):
#         # Se connecter avec l'utilisateur admin
#         self.client.login(username='adminuser', password='secret')

#     def test_create_view_status_code(self):
#         """
#         Tester que l'URL de création renvoie un statut 200 (OK)
#         """
#         response = self.client.get(reverse('fournisseur-add'))
#         self.assertEqual(response.status_code, 200)

#     def test_list_view_status_code(self):
#         """
#         Tester que l'URL de la liste renvoie un statut 200 (OK)
#         """
#         response = self.client.get(reverse('fournisseur-list'))
#         self.assertEqual(response.status_code, 200)


# class FournisseurTestUrlResponsesWithParameters(TestCase):
#     def setUp(self):
#         # Créer un fournisseur à utiliser pour les tests
#         self.fournisseur = Fournisseur.objects.create(nom="Apple", adresse="1 Infinite Loop")
#         self.user = User.objects.create_user(username='testuser', password='secret')
#         self.client.login(username='testuser', password='secret')

#     def test_detail_view_status_code(self):
#         """
#         Tester que l'URL des détails renvoie un statut 200 pour un ID valide
#         """
#         url = reverse('fournisseur-detail', args=[self.fournisseur.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_detail_view_status_code_invalid_id(self):
#         """
#         Tester que l'URL des détails renvoie un statut 404 pour un ID invalide
#         """
#         url = reverse('fournisseur-detail', args=[9999])  # ID non existant
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)


# class FournisseurTestUrlRedirect(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Créer un super-utilisateur pour les tests
#         cls.user = User.objects.create_superuser(username='adminuser', password='secret', email='admin@test.com')

#     def setUp(self):
#         # Connexion de l'utilisateur superuser pour le test
#         self.client.login(username='adminuser', password='secret')

#     def test_redirect_after_creation(self):
#         """
#         Tester qu'après la création d'un Fournisseur, l'utilisateur est redirigé correctement
#         """
#         response = self.client.post(reverse('fournisseur-add'), {
#             'nom': 'Nouveau Fournisseur',
#             'adresse': '123 Rue Test',
#         })

#         # Imprimer les erreurs de formulaire s'il y en a
#         if response.status_code == 200:
#             print(response.context['form'].errors)  # Affiche les erreurs de validation du formulaire

#         # Statut 302 = redirection
#         self.assertEqual(response.status_code, 302)

#         # Obtenir l'ID du fournisseur nouvellement créé
#         fournisseur_id = Fournisseur.objects.first().id
#         # Vérifier la redirection vers la page de détail du fournisseur
#         self.assertRedirects(response, reverse('fournisseur-detail', args=[fournisseur_id]))
