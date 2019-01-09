from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from pprint import pprint
import csv

from .models import Project, ProjectForm, UploadsForm, Target, Vulnerability

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

