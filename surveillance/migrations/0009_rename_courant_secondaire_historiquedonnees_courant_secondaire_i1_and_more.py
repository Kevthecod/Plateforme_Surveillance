# Generated by Django 5.1.1 on 2024-12-01 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance', '0008_remove_transformateur_courant_secondaire_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historiquedonnees',
            old_name='courant_secondaire',
            new_name='courant_secondaire_I1',
        ),
        migrations.AddField(
            model_name='historiquedonnees',
            name='courant_secondaire_I2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='historiquedonnees',
            name='courant_secondaire_I3',
            field=models.FloatField(null=True),
        ),
    ]
