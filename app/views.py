from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import WorkDayForm
from .models import WorkDay, Project
import datetime
import csv
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
        form = WorkDayForm(initial={'date': datetime.date.today().isoformat()},instance=WorkDay())
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
    project_filter = request.GET.get('project', 'all')
    date_to_filter = request.GET.get('dateto', '')
    date_from_filter = request.GET.get('datefrom', '')

    if project_filter != 'all':
        projects = Project.objects.filter(pk=project_filter)
    else:
        projects = Project.objects.all()

    all_projects = {}
    filter_list = Project.objects.all()

    for project in projects:
        times = WorkDay.objects.filter(project = project).order_by('date')
        if times:

            if date_from_filter != '':
                print date_from_filter
                times = times.filter(date__gt=date_from_filter)

            if date_to_filter != '':
                print date_to_filter
                times = times.filter(date__lt=date_to_filter)

            sort = request.GET.get('sort', 'none')
            if sort == 'date':
                times = times.order_by('date')
            elif sort == 'user':
                times = times.order_by('user__first_name')
            total_time = 0
            for time in times:
                total_time += float(time.days)
            all_projects[project.projectName] = {
                'project_id': project.pk,
                'times':times,
                'total_time':total_time,
            }

    filters = [{"label": "Project","name": "project", "options": filter_list}]

    return render(request,
                'app/viewprojects.html', {
                'projects': all_projects,
                'filters': filters,
                'date_to': date_to_filter,
                'date_from': date_from_filter
                })


@login_required(login_url='/user/login/')
def usersView(request):
    user_filter = request.GET.get('user', 'all')
    date_to_filter = request.GET.get('dateto', '')
    date_from_filter = request.GET.get('datefrom', '')
    print date_to_filter

    if user_filter != 'all':
        users = User.objects.filter(pk=user_filter)
    else:
        users = User.objects.all()
    all_users = {}
    filter_list = User.objects.all()
    for user in users:
        times = WorkDay.objects.filter(user = user).order_by('date')

        if date_from_filter != '':
            print date_from_filter
            times = times.filter(date__gt=date_from_filter)

        if date_to_filter != '':
            print date_to_filter
            times = times.filter(date__lt=date_to_filter)

        sort = request.GET.get('sort', 'none')
        if sort == 'date':
            times = times.order_by('date')
        elif sort == 'project':
            times = times.order_by('project')
        all_users[user] = times

    filters = [{"label": "User","name": "user", "options": filter_list}]

    return render(request, 'app/viewusers.html', {'users': all_users, 'filters': filters})


@login_required(login_url='/user/login/')
def getProjectCSV(request):
    project_filter = request.GET.get('project', 'all')
    date_to_filter = request.GET.get('dateto', '')
    date_from_filter = request.GET.get('datefrom', '')

    project = Project.objects.get(pk = project_filter)

    times = WorkDay.objects.filter(project = project).order_by('date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + project.projectName + '"'

    if times:

        if date_from_filter != '':
            print date_from_filter
            times = times.filter(date__gt=date_from_filter)
            response['Content-Disposition'] += "_" + date_from_filter

        if date_to_filter != '':
            print date_to_filter
            times = times.filter(date__lt=date_to_filter)
            response['Content-Disposition'] += "_" + date_to_filter

        sort = request.GET.get('sort', 'none')
        if sort == 'date':
            times = times.order_by('date')
        elif sort == 'user':
            times = times.order_by('user__first_name')


    writer = csv.writer(response)
    writer.writerow(['Date', 'User', 'Project', 'Days'])
    for time in times:
        writer.writerow([time.date, time.user, time.project, time.days])

    return response
