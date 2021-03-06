# Generated by Django 2.1.4 on 2019-01-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0003_project_project_lazyt_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_LazyT_progress',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_CP',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_FB',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_client_company',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_client_contact_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_nessus_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_qualys_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_test_dates',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_tester_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_tester_phone',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_tester_qualifications',
            field=models.CharField(max_length=200),
        ),
    ]
