from django.db import models
from django.db.models.functions import Concat
from django.forms import ModelForm
from datetime import datetime
from django.contrib.postgres.fields import ArrayField


class Project(models.Model):
    project_FB = models.CharField(max_length=5, default=12345)
    project_CP = models.CharField(max_length=5, default=12345)
    project_client_company = models.CharField(max_length=50,  default="Default Company")
    project_client_contact_name = models.CharField(max_length=50, default="Default Contact")
    project_test_dates = models.CharField(max_length=200, default="Dec 12-24th 2019")
    project_tester_name = models.CharField(max_length=50, default="Jill Ferron")
    project_tester_email = models.EmailField(default="jill@firstbase.co.uk")
    project_tester_qualifications = models.CharField(max_length=200, default="MSc")
    project_tester_phone = models.CharField(max_length=11 , default="01234756595")
    project_targets = models.TextField(default="127.0.0.1")
    project_qualys_file = models.FileField( blank=True, null=True)
    project_nessus_file = models.FileField( blank=True, null=True)
    project_lazyt_progress = models.PositiveSmallIntegerField(null=True, default=0)
    project_created_date = models.DateTimeField(auto_now_add=True, null=True)
    def project_full_name(self):
        return 'FB'+str(self.project_FB)+'-CP'+str(self.project_CP)+'-'+str(self.project_client_company)
    def __str__(self):
        return self.project_full_name()

class ProjectForm(ModelForm):
    class Meta:
            model = Project
            fields = ["project_FB","project_CP", "project_client_company", "project_client_contact_name", "project_test_dates", "project_tester_name", "project_tester_email", "project_tester_qualifications", "project_tester_phone", "project_targets", "project_qualys_file", "project_nessus_file"]

class UploadsForm(ModelForm):
    class Meta:
            model = Project
            fields = ["project_nessus_file","project_qualys_file"]


class Target(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    target_IP = models.GenericIPAddressField()
    target_status = models.BooleanField(null=True, default=1)
    def __str__(self):
        return self.target_IP
    
class Vulnerability(models.Model):
    vulnerability_target = models.GenericIPAddressField(null=True)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vulnerability_Dradis_ID = models.TextField()
    vulnerability_ports = models.TextField()
    vulnerability_protocol = models.TextField(null=True)
    vulnerability_outputs = models.TextField(null=True)
    vulnerability_source = models.TextField(null=True)
    vulnerability_source_id = models.PositiveIntegerField(null=True)
    vulnerability_source_name = models.TextField(null=True)
    vulnerability_reporting = models.CharField(null=True, max_length=500, default="1_maybe")
    vulnerability_FB_name = models.CharField(max_length=500, blank=True)
    def __str__(self):
        return self.vulnerability_Dradis_ID

class Rules(models.Model):
    rules_file = models.FileField( blank=True, null=True)
    rules_created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.rules_created_date

class RulesForm(ModelForm):
    class Meta:
            model = Rules
            fields = ["rules_file"]

class Rule(models.Model):
    rule_rules_id = models.PositiveIntegerField(null=True)
    rule_FB_name = models.CharField(max_length=500)
    rule_FB_id = models.PositiveIntegerField(null=True)
    rule_plugin_id = models.PositiveIntegerField(null=True)
    rule_source = models.CharField(max_length=100)
    rule_source_name = models.CharField(max_length=500, null=True)
    rule_created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.rule_FB_name

class FBRule(models.Model):
    rule_FB_name = models.CharField(max_length=500)
    rule_nessus_plugin_ids = ArrayField(base_field=models.IntegerField(), default=[])
    rule_qualys_plugin_ids = ArrayField(base_field=models.IntegerField(), default=[])
    rule_created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.rule_FB_name