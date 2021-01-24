# Generated by Django 3.1.5 on 2021-01-21 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0002_auto_20210121_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='file_name',
            field=models.CharField(default='1', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='text',
            name='text_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]