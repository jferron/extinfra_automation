# Generated by Django 2.1.4 on 2019-01-03 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_FB', models.PositiveIntegerField()),
                ('project_CP', models.PositiveIntegerField()),
                ('project_client_company', models.TextField()),
                ('project_client_contact_name', models.TextField()),
                ('project_test_dates', models.TextField()),
                ('project_tester_name', models.TextField()),
                ('project_tester_email', models.EmailField(max_length=254)),
                ('project_tester_qualifications', models.TextField()),
                ('project_tester_phone', models.TextField()),
                ('project_targets', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_IP', models.GenericIPAddressField()),
                ('Project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automation.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vulnerability_Dradis_ID', models.PositiveIntegerField()),
                ('vulnerability_ports', models.TextField()),
                ('vulnerability_outputs', models.TextField()),
                ('Target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automation.Target')),
            ],
        ),
    ]
