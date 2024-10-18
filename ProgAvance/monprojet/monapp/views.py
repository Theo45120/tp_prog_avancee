from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from .models import *
from django.db.models import Min
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.contrib import messages  # Assurez-vous d'importer messages


from .forms import *
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
import time

from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

# Vérifier si l'utilisateur est un superuser
def superuser_required(user):
    return user.is_superuser

""" def home(request):
    if request.GET and request.GET["test"]:
        raise Http404
    return HttpResponse("Bonjour Monde!") """
    #return HttpResponse("<h1>Hello World</h1>")

def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

def contact(request):
    #dom = "<h1>Nous contacter</h1>\n<p>Formulaire de contact disponible prochainement</p>"
    #return HttpResponse(dom)
    return render(request, 'monapp/contact.html')     


def about(request):
    #return HttpResponse("<h1>Qui sommes-nous ?</h1>")
    return render(request, 'monapp/about.html')     


def hello(request, param):
    return HttpResponse("<h1>Hello "+param+"! </h1>")

""" def listProducts(request):
    listeProduits = Product.objects.all()
    txt = '<h1>VOICI LES PRODUITS</h1><ul>'
    for p in listeProduits :
        txt += '<li>'+str(p.name)+'</li>'
    txt += '</ul>'
    return HttpResponse(txt)
 """

def listProducts(request):
    prdcts = Product.objects.all()
    return render(request, 'monapp/list_products.html',{'prdcts': prdcts})     

def listStatus(request):
    listeStatus = Status.objects.all()
    txt = '<h1>VOICI LES STATUS</h1><ul>'
    for s in listeStatus :
        txt += '<li>'+str(s.libelle)+'</li>'
    txt += '</ul>'
    return HttpResponse(txt)

def listItems(request):
    items = ProductItem.objects.all()
    return render(request, 'monapp/list_items.html',{'items': items})

def listAttributes(request):
    attributes = ProductAttribute.objects.all()
    return render(request, 'monapp/list_attributes.html',{'attributes': attributes})     

class HomeView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)    
    
    
# class ContactView(TemplateView):
#     template_name = "monapp/contact.html"
        
#     def get_context_data(self, **kwargs):
#         context = super(ContactView, self).get_context_data(**kwargs)
#         context['titreh1'] = "Nous contacter"
#         context['paragraphe'] = "Formulaire de contact disponible prochainement"
#         return context

#     def post(self, request, **kwargs):
#         return render(request, self.template_name)


class HomeViewParam(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeViewParam, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"+ " " +kwargs['param']
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name) 

class ProductListView(ListView):
    model = Product
    template_name = "monapp/list_products.html"
    context_object_name = "products"

    def get_queryset(self):
        # Fetch the products with their lowest supplier price
        query = self.request.GET.get('search')
        
        # Start with base queryset
        queryset = Product.objects.all()
        
        # Annotate each product with the lowest price from FournisseurProduit
        queryset = queryset.annotate(
            min_price=Min('fournisseurproduit__price_ttc')
        )
        
        # Filter by search query if present
        if query:
            queryset = queryset.filter(name__icontains=query)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "monapp/detail_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    
    def post(self, request, *args, **kwargs):
        # Récupérer le produit et le fournisseur depuis les paramètres du formulaire
        product = self.get_object()  # Récupère le produit actuel
        fournisseur_id = request.POST.get('fournisseur_id')
        quantity = request.POST.get('quantity')

        fournisseur_produit = get_object_or_404(FournisseurProduit, produit=product, fournisseur_id=fournisseur_id)

        try:
            # Valider et vérifier la quantité saisie
            quantity = int(quantity)
            if quantity <= fournisseur_produit.stock:
                # Réduire le stock de la quantité validée
                fournisseur_produit.stock -= quantity
                fournisseur_produit.save()

                # Ajouter d'autres actions ici, par exemple, création de commande
                return redirect('product-detail', product.id)
            else:
                return HttpResponseBadRequest("La quantité dépasse le stock disponible.")
        except ValueError:
            return HttpResponseBadRequest("Quantité invalide.")

# class ItemListView(ListView):
#     model = ProductItem
#     template_name = "monapp/list_items.html"
#     context_object_name = "items"

#     def get_queryset(self ) :
#         return ProductItem.objects.order_by("code")
    
#     def get_context_data(self, **kwargs):
#         context = super(ItemListView, self).get_context_data(**kwargs)
#         context['titre'] = "Liste des items"
#         return context

class ItemsDetailView(DetailView):
    model = ProductItem
    template_name = "monapp/detail_item.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super(ItemsDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail item"
        return context
    
# class AttributeListView(ListView):
#     model = ProductAttribute
#     template_name = "monapp/list_attributes.html"
#     context_object_name = "attributes"
    
#     def get_context_data(self, **kwargs):
#         context = super(AttributeListView, self).get_context_data(**kwargs)
#         context['titre'] = "Liste des attributs"
#         return context
    
class ConnectView(LoginView):
    template_name = 'monapp/login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'home.html',{'titreh1':"hello "+username+", you're connected"})
        else:
            return render(request, 'monapp/register.html')

class RegisterView(TemplateView):
    template_name = 'monapp/register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monapp/login.html')
        else:
            return render(request, 'monapp/register.html')

class DisconnectView(TemplateView):
    template_name = 'monapp/logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
def ContactView(request):
    titreh1 = "Contact us !"
    
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
            # Si tu veux rediriger après envoi de l'email (optionnel)
            return redirect('email-sent')
            #return render(request, "monapp/contact.html", {'titreh1': "Message sent!"})
    else:
        form = ContactUsForm()  # Crée une instance vide du formulaire si GET ou autre

    return render(request, "monapp/contact.html", {'titreh1': titreh1, 'form': form})

class EmailSentView(TemplateView):
    template_name = 'monapp/emailSent.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
# Vérifier si l'utilisateur est un superuser
def superuser_required(user):
    return user.is_superuser


# Ajout du décorateur login_required à une CBV

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ProductCreateView(CreateView):
    model = Product  # Define the model you're working with
    form_class = ProductForm  # Define the form class you're using
    template_name = 'monapp/new_product.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)


# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'monapp/update_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les fournisseurs qui ne sont pas encore associés à ce produit
        context['fournisseurs_non_associes'] = Fournisseur.objects.exclude(
            id__in=self.object.fournisseurproduit_set.values_list('fournisseur_id', flat=True)
        )
        return context

    def form_valid(self, form):
        product = form.save()

        if 'remove_fournisseur_id' in self.request.POST:
            # Action de suppression
            remove_fournisseur_id = self.request.POST.get('remove_fournisseur_id')
            if remove_fournisseur_id:
                fournisseur_produit = get_object_or_404(FournisseurProduit, id=remove_fournisseur_id)
                fournisseur_produit.delete()
                messages.success(self.request, f"Le fournisseur {fournisseur_produit.fournisseur.nom} a été retiré avec succès.")
                return redirect('product-update', pk=product.pk)
        else:

            # Mise à jour des fournisseurs déjà associés
            for fournisseur_produit in product.fournisseurproduit_set.all():
                new_prix = self.request.POST.get(f"fournisseur_prix_{fournisseur_produit.fournisseur.id}")
                new_stock = self.request.POST.get(f"fournisseur_stock_{fournisseur_produit.fournisseur.id}")

                if new_prix:
                    try:
                        fournisseur_produit.price_ttc = Decimal(new_prix)
                    except (ValueError, InvalidOperation):
                        messages.error(self.request, f"Le prix saisi pour {fournisseur_produit.fournisseur.nom} est invalide.")
                        return self.form_invalid(form)

                # Vérification de la condition de stock
                if new_stock and int(new_stock) < fournisseur_produit.stock:
                    messages.error(self.request, f"La nouvelle quantité de stock pour {fournisseur_produit.fournisseur.nom} doit être supérieure ou égale au stock actuel.")
                    return self.form_invalid(form)

                # Calculer la différence de stock
                difference_stock = int(new_stock) - fournisseur_produit.stock
                if difference_stock > 0:
                    Commande.objects.create(
                        produit=product,
                        fournisseur=fournisseur_produit.fournisseur,
                        quantite=difference_stock,
                        statut='en_preparation'
                    )
                fournisseur_produit.save()

            # Ajout de nouveaux fournisseurs avec leurs prix
            for fournisseur in Fournisseur.objects.all():
                price_ttc = self.request.POST.get(f"new_fournisseur_prix_{fournisseur.id}")
                stock = self.request.POST.get(f"new_fournisseur_stock_{fournisseur.id}")

                if price_ttc and stock:
                    try:
                        fournisseur_produit = FournisseurProduit.objects.create(
                            produit=product,
                            fournisseur=fournisseur,
                            price_ttc=Decimal(price_ttc),
                            stock=0
                        )

                        # Créer une commande pour ajouter le stock
                        Commande.objects.create(
                            produit=product,
                            fournisseur=fournisseur,
                            quantite=int(stock),
                            statut='en_preparation'
                        )
                    except (ValueError, InvalidOperation):
                        messages.error(self.request, f"Le prix saisi pour le nouveau fournisseur {fournisseur.nom} est invalide.")
                        return self.form_invalid(form)

            #messages.success(self.request, "Le produit a été mis à jour avec succès.")
            return redirect('product-detail', product.id)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "monapp/delete_product.html"
    success_url = reverse_lazy('product-list')  # URL to redirect to after successful deletion

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ItemCreateView(CreateView):
    model = ProductItem  # Define the model you're working with
    form_class = ItemForm  # Define the form class you're using
    template_name = 'monapp/new_item.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('items-detail', item.id)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ItemUpdateView(UpdateView):
    model = ProductItem  # Define the model you're working with
    form_class = ItemForm  # Define the form class you're using
    template_name = 'monapp/update_item.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('items-detail', item.id)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class ItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "monapp/delete_item.html"
    success_url = reverse_lazy('items-list')  # URL to redirect to after successful deletion

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class AttributeCreateView(CreateView):
    model = ProductAttribute  # Define the model you're working with
    form_class = AttributeForm  # Define the form class you're using
    template_name = 'monapp/new_attribute.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attribute = form.save()
        return redirect('attributes-list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class AttributeUpdateView(UpdateView):
    model = ProductAttribute  # Define the model you're working with
    form_class = AttributeForm  # Define the form class you're using
    template_name = 'monapp/update_attribute.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attribute = form.save()
        return redirect('attributes-list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class AttributeDeleteView(DeleteView):
    model = ProductAttribute
    template_name = "monapp/delete_attribute.html"
    success_url = reverse_lazy('attributes-list')  # URL to redirect to after successful deletion

class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "monapp/list_attributes.html"
    context_object_name = "productattributes"

    # def get_queryset(self ):
    #     return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
        # Filtre les produits par nom (insensible à la casse)
            return ProductAttribute.objects.filter(name__icontains=query)
        
        # Si aucun terme de recherche, retourner tous les produits
        return ProductAttribute.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context

class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "monapp/detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context
    
class ProductItemListView(ListView):
    model = ProductItem
    template_name = "monapp/list_items.html"
    context_object_name = "productitems"

    # def get_queryset(self ):
    #    return ProductItem.objects.select_related('product').prefetch_related('attributes')

    def get_queryset(self ):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
        # Filtre les produits par nom (insensible à la casse)
            return ProductItem.objects.filter(code__icontains=query)
        
        # Si aucun terme de recherche, retourner tous les produits
        return ProductItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context
    
class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "monapp/detail_item.html"
    context_object_name = "productitem"

    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        # Récupérer les attributs associés à cette déclinaison
        context['attributes'] = self.object.attributes.all()
        return context
    
class ProductAttributeValueListView(ListView):
    model = ProductAttributeValue
    template_name = "monapp/list_attributesValue.html"
    context_object_name = "productAttributeValue"

    # def get_queryset(self ):
    #     return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
        # Filtre les produits par nom (insensible à la casse)
            return ProductAttributeValue.objects.filter(product_attribute__name__icontains=query)
        
        # Si aucun terme de recherche, retourner tous les produits
        return ProductAttributeValue.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des valeurs d'attributs"
        return context

class ProductAttributeValueDetailView(DetailView):
    model = ProductAttributeValue
    template_name = "monapp/detail_attributeValue.html"
    context_object_name = "productAttributeValue"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        return context

def avancer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    # Si la commande est encore en préparation
    if commande.statut == 'en_preparation':
        commande.statut = 'passee'
        commande.save()
        time.sleep(5)  # Attendre 20 secondes avant de passer à l'étape suivante

    # Si la commande est passée mais pas encore reçue
    if commande.statut == 'passee':
        commande.statut = 'recue'
        commande.save()
        time.sleep(5)  # Attendre 20 secondes avant de marquer la commande comme reçue

    return redirect('commande-detail', commande_id=commande.id)  # Redirige vers le détail de la commande après mise à jour


## POUR AJAX,
def actualiser_statut_commande(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    # Change le statut automatiquement
    commande.changer_statut_automatiquement()
    return JsonResponse({'statut': commande.statut})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class CommandeListView(ListView):
    model = Commande
    template_name = 'monapp/list_commande.html'
    context_object_name = 'commandes'
    ordering = ['-date_commande']  # Trier par date_commande du plus récent au plus ancien


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class CommandeDetailView(DetailView):
    model = Commande
    template_name = 'monapp/commande_detail.html'
    context_object_name = 'commande'

    def get_object(self):
        # Récupérer l'objet commande en fonction de l'ID fourni dans l'URL
        commande_id = self.kwargs.get('commande_id')
        return get_object_or_404(Commande, id=commande_id)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class CommandeDeleteView(DeleteView):
    model = Commande
    template_name = "monapp/delete_commande.html"
    success_url = reverse_lazy('commande-list')  # URL to redirect to after successful deletion
class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "monapp/list_fournisseurs.html"  # Le template à utiliser pour afficher la liste
    context_object_name = "fournisseurs"  # Le nom de l'objet dans le contexte du template

    def get_queryset(self):
        """
        Surcouche pour filtrer les résultats en fonction de la recherche.
        Récupère le terme de recherche dans la requête GET.
        """
        query = self.request.GET.get('search')
        if query:
            # Filtrer les fournisseurs par nom (insensible à la casse)
            return Fournisseur.objects.filter(nom__icontains=query)
        
        # Si aucun terme de recherche, retourner tous les fournisseurs
        return Fournisseur.objects.all()

    def get_context_data(self, **kwargs):
        """
        Ajouter des données supplémentaires au contexte de la vue.
        """
        context = super(FournisseurListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des fournisseurs"  # Un titre personnalisé pour le menu
        return context

class FournisseurDetailView(DetailView):
    model = Fournisseur
    template_name = "monapp/detail_fournisseur.html"
    context_object_name = "fournisseur"

    def get_context_data(self, **kwargs):
        """
        Ajouter les produits vendus par le fournisseur au contexte.
        """
        context = super(FournisseurDetailView, self).get_context_data(**kwargs)
        # Récupérer les produits liés au fournisseur
        produits_vendus = FournisseurProduit.objects.filter(fournisseur=self.object)
        context['produits_vendus'] = produits_vendus
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class FournisseurCreateView(CreateView):
    model = Fournisseur  # Le modèle utilisé
    form_class = FournisseurForm  # Le formulaire pour créer un fournisseur
    template_name = 'monapp/new_fournisseur.html'  # Le template pour afficher le formulaire

    def form_valid(self, form) -> HttpResponse:
        # Enregistrer le fournisseur et rediriger vers sa page de détails
        fournisseur = form.save()
        return redirect('fournisseur-detail', fournisseur.id)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class FournisseurDeleteView(DeleteView):
    model = Fournisseur  # Le modèle utilisé pour cette vue
    template_name = "monapp/delete_fournisseur.html"  # Le template pour confirmer la suppression
    success_url = reverse_lazy('fournisseur-list')  # Redirection après la suppression réussie

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    form_class = FournisseurUpdateForm
    template_name = 'monapp/update_fournisseur.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits_associes'] = FournisseurProduit.objects.filter(fournisseur=self.object)
        context['produits_non_associes'] = Product.objects.exclude(
            id__in=self.object.fournisseurproduit_set.values_list('produit_id', flat=True)
        )
        return context

    def form_valid(self, form):
        fournisseur = form.save()

        if 'remove_fournisseur_id' in self.request.POST:
            # Action de suppression
            remove_fournisseur_id = self.request.POST.get('remove_fournisseur_id')
            if remove_fournisseur_id:
                fournisseur_produit = get_object_or_404(FournisseurProduit, id=remove_fournisseur_id)
                fournisseur_produit.delete()
                messages.success(self.request, f"Le produit {fournisseur_produit.produit.name} a été retiré avec succès.")
                return redirect('fournisseur-update', pk=fournisseur.pk)
        else:
            # Action de mise à jour
            for fournisseur_produit in fournisseur.fournisseurproduit_set.all():
                new_prix = self.request.POST.get(f"fournisseur_prix_{fournisseur_produit.produit.id}")
                new_stock = self.request.POST.get(f"fournisseur_stock_{fournisseur_produit.produit.id}")

                if new_prix:
                    fournisseur_produit.price_ttc = Decimal(new_prix)

                if new_stock:
                    try:
                        new_stock_int = int(new_stock)
                        if new_stock_int < fournisseur_produit.stock:
                            messages.error(self.request, f"La nouvelle quantité de stock pour {fournisseur_produit.produit.name} doit être supérieure ou égale au stock actuel.")
                            return self.form_invalid(form)

                        difference_stock = new_stock_int - fournisseur_produit.stock
                        if difference_stock > 0:
                            Commande.objects.create(
                                produit=fournisseur_produit.produit,
                                fournisseur=fournisseur,
                                quantite=difference_stock,
                                statut='en_preparation'
                            )
                        fournisseur_produit.stock = new_stock_int
                    except ValueError:
                        messages.error(self.request, f"La valeur du stock pour {fournisseur_produit.produit.name} est invalide.")
                        return self.form_invalid(form)

                fournisseur_produit.save()

            # Ajouter de nouveaux produits
            for produit in Product.objects.all():
                price_ttc = self.request.POST.get(f"new_fournisseur_prix_{produit.id}")
                stock = self.request.POST.get(f"new_fournisseur_stock_{produit.id}")

                if price_ttc and stock:
                    try:
                        fournisseur_produit = FournisseurProduit.objects.create(
                            produit=produit,
                            fournisseur=fournisseur,
                            price_ttc=Decimal(price_ttc),
                            stock=0
                        )
                        Commande.objects.create(
                            produit=produit,
                            fournisseur=fournisseur,
                            quantite=int(stock),
                            statut='en_preparation'
                        )
                    except ValueError:
                        messages.error(self.request, f"Erreur lors de la création de la relation pour le produit {produit.name}.")
                        return self.form_invalid(form)

            messages.success(self.request, "Modifications enregistrées avec succès.")
            return redirect('fournisseur-detail', fournisseur.id)