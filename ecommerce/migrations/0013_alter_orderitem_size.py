# Generated by Django 4.2.3 on 2023-07-15 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_orderitem_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(choices=[('M', 'M   (17.7"/12.6")'), ('L', 'L   (26.6"/18.9")'), ('XL', 'XL   (35.4"/25.2")')], max_length=30),
        ),
    ]