from django.conf import settings
from django.urls import path
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:project_id>', views.project, name='project'),
    path('project/<int:project_id>/nessus', views.nessus_file, name='nessus_file'),
    path('project/<int:project_id>/nessus/parse', views.nessus_parse, name='nessus_parse'),
    path('project/<int:project_id>/qualys/parse', views.qualys_parse, name='qualys_parse'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)