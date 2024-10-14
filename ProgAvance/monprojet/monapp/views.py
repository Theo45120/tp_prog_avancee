from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import *
from django.db.models import Min
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail

from .forms import AttributeForm, ContactUsForm, ItemForm, ProductForm, ProductUpdateForm
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import time

from django.http import JsonResponse


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
    
# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product  # Define the model you're working with
    form_class = ProductForm  # Define the form class you're using
    template_name = 'monapp/new_product.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)


@method_decorator(login_required, name='dispatch')
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

        # Mise à jour des fournisseurs déjà associés (sans ajouter au stock deux fois)
        for fournisseur_produit in product.fournisseurproduit_set.all():
            new_prix = self.request.POST.get(f"fournisseur_prix_{fournisseur_produit.fournisseur.id}")
            new_stock = self.request.POST.get(f"fournisseur_stock_{fournisseur_produit.fournisseur.id}")

            if new_prix:
                fournisseur_produit.price_ttc = Decimal(new_prix)  # Assure-toi de bien utiliser Decimal pour les prix

            # Calculer la différence de stock (si le nouveau stock est plus élevé)
            difference_stock = int(new_stock) - fournisseur_produit.stock
            if difference_stock > 0:
                # Ne pas directement toucher au stock ici
                # Créer uniquement la commande pour gérer l'ajout du stock plus tard
                Commande.objects.create(
                    produit=product,
                    fournisseur=fournisseur_produit.fournisseur,
                    quantite=difference_stock,
                    statut='en_preparation'  # La commande commence en préparation
                )
        # Sauvegarder les changements dans la base de données
            fournisseur_produit.save()

        # Ajout de nouveaux fournisseurs avec leur prix (sans modifier directement le stock ici)
        for fournisseur in Fournisseur.objects.all():
            price_ttc = self.request.POST.get(f"new_fournisseur_prix_{fournisseur.id}")
            stock = self.request.POST.get(f"new_fournisseur_stock_{fournisseur.id}")

            if price_ttc and stock:
                # Créer la relation fournisseur-produit avec le stock à 0
                fournisseur_produit = FournisseurProduit.objects.create(
                    produit=product,
                    fournisseur=fournisseur,
                    price_ttc=price_ttc,
                    stock=0  # Stock initial à 0, il sera ajouté via la commande
                )

                # Créer une commande pour le nouveau stock (avec statut en préparation)
                Commande.objects.create(
                    produit=product,
                    fournisseur=fournisseur,
                    quantite=int(stock),
                    statut='en_preparation'
                )

        return redirect('product-detail', product.id)

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "monapp/delete_product.html"
    success_url = reverse_lazy('product-list')  # URL to redirect to after successful deletion

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class ItemCreateView(CreateView):
    model = ProductItem  # Define the model you're working with
    form_class = ItemForm  # Define the form class you're using
    template_name = 'monapp/new_item.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('items-detail', item.id)

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
    model = ProductItem  # Define the model you're working with
    form_class = ItemForm  # Define the form class you're using
    template_name = 'monapp/update_item.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('items-detail', item.id)

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "monapp/delete_item.html"
    success_url = reverse_lazy('items-list')  # URL to redirect to after successful deletion

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class AttributeCreateView(CreateView):
    model = ProductAttribute  # Define the model you're working with
    form_class = AttributeForm  # Define the form class you're using
    template_name = 'monapp/new_attribute.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attribute = form.save()
        return redirect('attributes-list')

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
class AttributeUpdateView(UpdateView):
    model = ProductAttribute  # Define the model you're working with
    form_class = AttributeForm  # Define the form class you're using
    template_name = 'monapp/update_attribute.html'  # Define the template for rendering
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attribute = form.save()
        return redirect('attributes-list')

# Ajout du décorateur login_required à une CBV
@method_decorator(login_required, name='dispatch')
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
        time.sleep(20)  # Attendre 20 secondes avant de passer à l'étape suivante

    # Si la commande est passée mais pas encore reçue
    if commande.statut == 'passee':
        commande.statut = 'recue'
        commande.save()
        time.sleep(20)  # Attendre 20 secondes avant de marquer la commande comme reçue

    return redirect('commande-detail', commande_id=commande.id)  # Redirige vers le détail de la commande après mise à jour


## POUR AJAX,
def actualiser_statut_commande(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    # Change le statut automatiquement
    commande.changer_statut_automatiquement()
    return JsonResponse({'statut': commande.statut})


class CommandeListView(ListView):
    model = Commande
    template_name = 'monapp/list_commande.html'
    context_object_name = 'commandes'