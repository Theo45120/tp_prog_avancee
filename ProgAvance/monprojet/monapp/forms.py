from django import forms
from .models import Product, ProductAttribute, ProductItem, Fournisseur, FournisseurProduit, ProductAttributeValue

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('status',)

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
        fields = ['name', 'code', 'status']  # Champs de base du produit

    # Champ supplémentaire pour les fournisseurs et le stock
    fournisseur_data = forms.CharField(widget=forms.HiddenInput(), required=False)  # Pour gérer les fournisseurs et le stock en JS

    def save(self, commit=True):
        # Sauvegarde du produit de base
        product = super().save(commit=False)

        # Si commit=True, on sauvegarde le produit
        if commit:
            product.save()

        # Gestion des fournisseurs et du stock (sans modification directe du stock ici)
        if 'fournisseur_data' in self.cleaned_data and self.cleaned_data['fournisseur_data']:
            fournisseur_data = self.cleaned_data['fournisseur_data']
            # Parser et traiter le JSON ou la chaîne contenant les données fournisseurs/stock
            # Par exemple, mettre à jour les relations entre le produit et les fournisseurs
            # NE PAS mettre à jour le stock directement ici !

        return product

class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = ['value', 'product_attribute', 'position']  # Champs du formulaire

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].required = True
        self.fields['product_attribute'].required = True
        self.fields['position'].required = False