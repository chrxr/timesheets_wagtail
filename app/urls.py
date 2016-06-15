from django.conf.urls import url, include
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='app/home.html'), name='home'),
    url(r'^user/logout/$', auth_views.logout, {'template_name': 'app/home.html'}, name='logout'),
    # Login and other user auth views provided by django built-in module
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^logtime/$', views.logTime, name='log-time'),
    url(r'^view-times/$', views.viewMyTimes, name='view-my-times'),
    url(r'^edit-time/([0-9]+)/$', views.editTime, name='edit-time'),
    url(r'^delete-time/([0-9]+)/$', views.deleteTime, name='delete-time'),
    url(r'^projects-view/$', views.projectsView, name='projects-view'),
    url(r'^users-view/$', views.usersView, name='users-view'),
    url(r'^get-project-csv/$', views.getProjectCSV, name='get-project-csv'),
    url(r'^signup/$', views.createAccount, name='create-account'),
]
