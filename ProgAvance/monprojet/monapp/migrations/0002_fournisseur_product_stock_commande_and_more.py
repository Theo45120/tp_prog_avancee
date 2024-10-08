# Generated by Django 5.1.1 on 2024-10-08 07:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField()),
                ('statut', models.CharField(choices=[('en_preparation', 'En préparation'), ('passee', 'Passée'), ('recue', 'Reçue')], default='en_preparation', max_length=20)),
                ('date_commande', models.DateTimeField(default=django.utils.timezone.now)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.product')),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='FournisseurProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.fournisseur')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.product')),
            ],
            options={
                'unique_together': {('produit', 'fournisseur')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='fournisseurs',
            field=models.ManyToManyField(through='monapp.FournisseurProduit', to='monapp.fournisseur'),
        ),
    ]
