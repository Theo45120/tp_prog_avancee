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
        fields = ['name', 'code','status']  # Champs de base du produit

    # Champ supplémentaire pour les fournisseurs et le stock
    fournisseur_data = forms.CharField(widget=forms.HiddenInput(), required=False)  # Pour gérer les fournisseurs et le stock en JS

    def save(self, commit=True):
        product = super().save(commit=False)
        
        # Sauvegarde du produit
        if commit:
            product.save()

        # Sauvegarde des relations fournisseur-produit (incluant le stock)
        if 'fournisseur_data' in self.cleaned_data:
            fournisseur_data = self.cleaned_data['fournisseur_data']
            # Process the fournisseur_data (you might need to parse JSON or a string here)
        
        return product
