# Generated by Django 5.1.1 on 2024-10-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0004_alter_product_options_remove_product_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fournisseurproduit',
            name='prix',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_ht',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_ttc',
        ),
        migrations.AddField(
            model_name='fournisseurproduit',
            name='price_ttc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Prix unitaire TTC'),
        ),
    ]
