# Generated by Django 4.2.3 on 2023-10-27 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offres', '0006_alter_product_category_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out of delivery', 'Out of delivery'), ('Delivered', 'Delivered')], max_length=200, null=True),
        ),
    ]
