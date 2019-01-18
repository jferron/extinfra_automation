from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from pprint import pprint
import csv
from openpyxl import load_workbook


from .models import Project, ProjectForm, UploadsForm, Target, Vulnerability, Rules, RulesForm, Rule, FBRule

def index(request):
    if request.method == 'POST':
         # POST, create new project and redirect to project page
         form = ProjectForm(request.POST, request.FILES)
         if form.is_valid():
             pprint(request.POST['project_targets'])
             new_project = form.save()
             split_targets(request.POST['project_targets'], new_project.id )
             project_path = 'project/'+ str(new_project.id)
             return HttpResponseRedirect(project_path)
    else:
         # GET, generate blank form
         form = ProjectForm()
    return render(request,'projects/project_form.html', {'form':form})


def project(request, project_id):
     project = get_object_or_404(Project, id=project_id)
     form = UploadsForm(request.POST, request.FILES)
     return render(request, 'projects/index.html', { 'project': project, 'form': form })    

def split_targets(targets, project_id):
     for line in targets.splitlines():
          target = Target(target_IP=line, Project_id=project_id)
          target.save()

def parse_nessus_data(nessus_file):
     file = open(nessus_file, "rU")
     reader = csv.reader(file, delimiter=',')
     for column in reader:
        print(column[0])

def nessus_file(request, project_id):
     project = get_object_or_404(Project, id=project_id)
     path = '/automation/uploads/'+str(project.project_nessus_file)
     return HttpResponseRedirect(path)

def nessus_parse(request, project_id):
     project = get_object_or_404(Project, id=project_id)
     reader = csv.reader(open(project.project_nessus_file.path,'r'))
     next(reader, None)
     for row in reader:
           Vulnerability.objects.get_or_create(vulnerability_source='Nessus', vulnerability_source_name=row[7], Project_id=project_id,vulnerability_target = row[4], vulnerability_source_id = row[0], vulnerability_ports = row[6],vulnerability_protocol = row[5], vulnerability_outputs = row[12])
     vulns = Vulnerability.objects.filter(Project_id=project.id, vulnerability_source='Nessus').order_by('vulnerability_target', 'vulnerability_source_id', 'vulnerability_ports')
     return render(request, 'projects/nessus.html', { 'project': project, 'vulns': vulns })    

def qualys_parse(request, project_id):
     project = get_object_or_404(Project, id=project_id)
     reader = list(csv.reader(open(project.project_qualys_file.path,'r'), delimiter=',', quotechar='"'))
     reader.pop()
     reader.pop()
     reader = reader[8:] 
     for row in reader:
           Vulnerability.objects.get_or_create(vulnerability_source='Qualys', vulnerability_source_name=row[6], Project_id=project_id,vulnerability_target = row[0], vulnerability_source_id = row[5], vulnerability_ports = row[9],vulnerability_protocol = row[10], vulnerability_outputs = row[21])
     vulns = Vulnerability.objects.filter(Project_id=project.id, vulnerability_source='Qualys').order_by('vulnerability_target', 'vulnerability_source_id', 'vulnerability_ports')
     return render(request, 'projects/qualys.html', { 'project': project, 'vulns': vulns })    

def rules_import(request):
    if request.method == 'POST':
         # POST, create new rules and redirect to rules page
         form = RulesForm(request.POST, request.FILES)
         if form.is_valid():
             new_rules = form.save()
          #    split_rules(request.POST['rules_file'])
             rules_path = str(new_rules.id)
             return HttpResponseRedirect(rules_path)
    else:
         # GET, generate blank form
         form = RulesForm()
    return render(request,'rules/rules_form.html', {'form':form})

def rules_parse(request, rules_id):
     rules = get_object_or_404(Rules, id=rules_id)
     rules_path = rules.rules_file.path
     wb = load_workbook(rules_path)
     qualys_worksheet = wb['Qualys']
     nessus_worksheet = wb['Nessus']

     for row in qualys_worksheet.rows:
          try:
               Rule.objects.get_or_create(rule_source='Qualys', rule_plugin_id = row[2].value, rule_source_name=row[3].value, rule_FB_name=row[4].value, rule_rules_id=rules_id )
          except:
               continue

     for row in nessus_worksheet.rows:
          try:
               Rule.objects.get_or_create(rule_source='Nessus', rule_plugin_id = row[2].value, rule_source_name=row[3].value, rule_FB_name=row[4].value, rule_rules_id=rules_id )
          except:
               continue

     parsed_rules = Rule.objects.filter(rule_rules_id=rules_id)
     return render(request, 'rules/index.html', {'wb2':wb, "rules_path":rules_path, "rules":parsed_rules, "rules_id":rules_id })    


def rules_generate(request, rules_id):
     uploaded_rules = Rule.objects.filter(rule_rules_id=rules_id)
     for rule in uploaded_rules: 
          if rule.rule_source == 'Nessus':
               fb_rule, created  = FBRule.objects.get_or_create(rule_FB_name=rule.rule_FB_name)
               if created:
                    pass
               else:
                    if int(rule.rule_plugin_id) not in fb_rule.rule_nessus_plugin_ids:
                         fb_rule.rule_nessus_plugin_ids.append(rule.rule_plugin_id)
                         fb_rule.save()
          if rule.rule_source == 'Qualys':
               fb_rule, created  = FBRule.objects.get_or_create(rule_FB_name=rule.rule_FB_name)
               if created:
                    pass
               else:
                    if int(rule.rule_plugin_id) not in fb_rule.rule_qualys_plugin_ids:
                         fb_rule.rule_qualys_plugin_ids.append(rule.rule_plugin_id)
                         fb_rule.save()
     fb_rules = FBRule.objects.all()
     return render(request, 'rules/fb_index.html', {"fb_rules":fb_rules })    


def scanner_results(request, project_id):
     qualys_parse(request, project_id)
     nessus_parse(request, project_id)
     project_scanner_vulns = Vulnerability.objects.filter(Project_id=project_id)
     fb_rules = FBRule.objects.all()
     for vuln in project_scanner_vulns:
          if vuln.vulnerability_source == 'Qualys':
               for rule in fb_rules:
                    if int(vuln.vulnerability_source_id) in rule.rule_qualys_plugin_ids:
                         vuln.vulnerability_reporting ="0_yes"
                         vuln.vulnerability_Dradis_ID = rule.id
                         vuln.vulnerability_FB_name = rule.rule_FB_name
               vuln.save()
          if vuln.vulnerability_source == 'Nessus':
               for rule in fb_rules:
                    if int(vuln.vulnerability_source_id) in rule.rule_nessus_plugin_ids:
                         vuln.vulnerability_reporting ="0_yes"
                         vuln.vulnerability_Dradis_ID = rule.id
                         vuln.vulnerability_FB_name = rule.rule_FB_name
               vuln.save()
     reported_vulns = Vulnerability.objects.filter(Project_id=project_id).order_by('vulnerability_reporting','vulnerability_FB_name', 'vulnerability_target')
     return render(request, 'projects/scanner_report.html', {"reported_vulns":reported_vulns })    