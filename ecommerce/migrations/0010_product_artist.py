# Generated by Django 4.2.3 on 2023-07-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_contactrequest_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='artist',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
