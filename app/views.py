from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import WorkDayForm
from .models import WorkDay, Project
import datetime
# Create your views here.

@login_required(login_url='/user/login/')
def logTime(request):
    if request.method == 'POST':
        form = WorkDayForm(request.POST, instance=WorkDay())
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user = request.user
            new_log.save()
            return HttpResponseRedirect(reverse('view-my-times'))
        else:
            return HttpResponse(form.errors)
    else:
        form = WorkDayForm(initial={'date': datetime.date.today()},instance=WorkDay())
    return render(request, 'app/workdayform.html', {'form': form})

@login_required(login_url='/user/login/')
def viewMyTimes(request):
    logged_in_user = request.user
    times = WorkDay.objects.filter(user=logged_in_user)

    return render(request, 'app/viewmytimes.html', {'times': times})

@login_required(login_url='/user/login/')
def editTime(request, time_id):
    time_to_edit = WorkDay.objects.get(pk=time_id)
    if request.method == 'POST':
        form = WorkDayForm(request.POST, instance=WorkDay())
        if form.is_valid():
            edited_form = form.save(commit=False)
            time_to_edit.date = edited_form.date
            time_to_edit.project = edited_form.project
            time_to_edit.hours = edited_form.hours
            time_to_edit.save()
            return HttpResponseRedirect(reverse('view-my-times'))
        else:
            return HttpResponse("ERROR!")
    else:
        form = WorkDayForm(instance=time_to_edit)
    return render(request, 'app/workdayform.html', {'form': form, 'action': 'edit'})

@login_required(login_url='/user/login/')
def deleteTime(request, time_id):
    time_to_delete = WorkDay.objects.get(pk=time_id)
    time_to_delete.delete()
    return HttpResponseRedirect(reverse('view-my-times'))

@login_required(login_url='/user/login/')
def projectsView(request):
    projects = Project.objects.all()
    all_projects = {}
    for project in projects:
        times = WorkDay.objects.filter(project = project)
        all_projects[project.projectName] = times
        # for field in all_projects[project.projectName]:
        #     print field.date
        print all_projects
    return render(request, 'app/viewprojects.html', {'projects': all_projects})

@login_required(login_url='/user/login/')
def usersView(request):
    users = User.objects.all()
    all_users = {}
    for user in users:
        times = WorkDay.objects.filter(user = user)
        all_users[user] = times
        # for field in all_projects[project.projectName]:
        #     print field.date
        print all_users
    return render(request, 'app/viewusers.html', {'users': all_users})
