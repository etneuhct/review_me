# Generated by Django 3.1.5 on 2021-02-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0007_auto_20210121_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='sentenceId',
            field=models.IntegerField(default=0),
        ),
    ]