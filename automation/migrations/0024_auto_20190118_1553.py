# Generated by Django 2.1.4 on 2019-01-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0023_vulnerability_vulnerability_fb_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerability',
            name='vulnerability_reporting',
            field=models.CharField(default='Maybe', max_length=500, null=True),
        ),
    ]
