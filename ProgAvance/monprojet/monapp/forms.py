from django import forms
from .models import Product, ProductAttribute, ProductItem, Fournisseur, FournisseurProduit

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('price_ttc', 'status')

class ItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'

class AttributeForm(forms.ModelForm):
    
    class Meta :
        model = ProductAttribute
        fields = '__all__'

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'price_ht', 'price_ttc', 'status', 'fournisseurs']

    # Ajouter un champ pour gérer les prix des fournisseurs
    fournisseur_prix = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    def save(self, commit=True):
        product = super().save(commit=False)
        # Gérer l'association des fournisseurs et leurs prix
        fournisseur_ids = self.cleaned_data['fournisseurs']
        prix = self.cleaned_data['fournisseur_prix']

        for fournisseur in fournisseur_ids:
            FournisseurProduit.objects.create(
                produit=product,
                fournisseur=fournisseur,
                prix=prix  # Le prix doit être fourni
            )

        if commit:
            product.save()
        return product
