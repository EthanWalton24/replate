# Generated by Django 4.2.3 on 2023-07-07 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_alter_contactrequest_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Complete', 'Complete')], default='Open', max_length=15),
        ),
    ]
