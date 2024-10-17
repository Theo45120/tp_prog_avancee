from xml.etree.ElementInclude import include
from django.urls import path

from monapp import admin
from .import views
from django.views.generic import *
from .views import actualiser_statut_commande

urlpatterns=[
    #path("", views.home, name="home"),
    #path("home/<param>",views.accueil ,name='accueil'),
    #path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    #path("hello/<param>", views.hello, name="about"),
    path("produits", views.listProducts, name="produits"),
    path("status", views.listStatus, name="status"),
    path("items", views.listItems, name="items"),
    path("attributes", views.listAttributes, name="attributes"),
    path("home", views.HomeView.as_view(), name="home"),
    #path("contact", views.ContactView.as_view()),
    path("contact", views.ContactView, name="contact"),
    path("home/<param>", views.HomeViewParam.as_view()),
    path("product/list",views.ProductListView.as_view(),name="product-list"),
    path("product/<pk>",views.ProductDetailView.as_view(), name="product-detail"), # pk est l id, on peut mettre ce que l on veut en name
    #path("items/list",views.ItemListView.as_view(),name="items-list"),
    path("items/list",views.ProductItemListView.as_view(),name="items-list"),
    #path("items/<pk>",views.ItemsDetailView.as_view(), name="items-detail"),
    path("items/<pk>",views.ProductItemDetailView.as_view(), name="items-detail"),
    #path("attributes/list",views.AttributeListView.as_view(),name="attributes-list"),
    path("attributes/list",views.ProductAttributeListView.as_view(), name="attributes-list"),
    path("login",views.ConnectView.as_view(),name="login"),
    path("register",views.RegisterView.as_view(),name="register"),
    path("logout",views.DisconnectView.as_view(),name="logout"),
    path("email-sent",views.EmailSentView.as_view(),name="email-sent"),
    path("product/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("product/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("product/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),
    path("item/add/",views.ItemCreateView.as_view(), name="item-add"),
    path("item/<pk>/update/",views.ItemUpdateView.as_view(), name="item-update"),
    path("item/<pk>/delete/",views.ItemDeleteView.as_view(), name="item-delete"),
    path("attribut/add/",views.AttributeCreateView.as_view(), name="attribute-add"),
    path("attribut/<pk>/update/",views.AttributeUpdateView.as_view(), name="attribute-update"),
    path("attribut/<pk>/delete/",views.AttributeDeleteView.as_view(), name="attribute-delete"),
    path("attribut/<pk>",views.ProductAttributeDetailView.as_view(), name="attribute-detail"),
    path("attributValue/list",views.ProductAttributeValueListView.as_view(), name="attributeValue-list"),
    path("attributValue/<pk>",views.ProductAttributeValueDetailView.as_view(), name="attributeValue-detail"),
    path('commande/<int:commande_id>/avancer/', views.avancer_commande, name='avancer-commande'),
    path('commande/<int:commande_id>/', views.CommandeDetailView.as_view(), name='commande-detail'),
    path('commande/<pk>/delete/', views.CommandeDeleteView.as_view(), name="commande-delete"),



    # URL de l'api AJAX
    path('commande/<int:commande_id>/actualiser_statut/', actualiser_statut_commande, name='actualiser-statut-commande'),
    path('commandes/', views.CommandeListView.as_view(), name='commande-list'),


]