# Generated by Django 4.2.3 on 2023-07-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_remove_customer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Hip-Hop/Rap', 'Hip-Hop/Rap'), ('R&B/Soul', 'R&B/Soul'), ('Pop', 'Pop'), ('Dance', 'Dance')], default='tops', max_length=19),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
