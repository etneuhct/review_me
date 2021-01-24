# Generated by Django 3.1.5 on 2021-01-21 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0005_word_verdict'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_na',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='category',
            field=models.CharField(choices=[('1', 'Non Inclusif'), ('2', 'Inclusif')], max_length=20),
        ),
    ]
