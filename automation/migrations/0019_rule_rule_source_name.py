# Generated by Django 2.1.4 on 2019-01-18 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0018_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='rule_source_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
