from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import views, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import WorkDayForm, CreateAccountForm, AddProjectForm
from .models import WorkDay, Project
import datetime
import csv
import operator
# Create your views here.

def createAccount(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session['user_name'] = new_user.username
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('log-time'));
        else:
            return render(request, 'registration/signupform.html', {'form': form})
    else:
        form = CreateAccountForm()

    return render(request, 'registration/signupform.html', {'form': form})

@login_required(login_url='/user/login/')
def logTime(request):
    date_today = datetime.date.today()
    day_today = datetime.date.weekday(date_today)
    week_beginning = date_today - datetime.timedelta(days=day_today)
    week_ending = week_beginning + datetime.timedelta(days=(5-day_today))

    weekly_times = WorkDay.objects.filter(date__gte=week_beginning, date__lte=week_ending, user=request.user)
    print(weekly_times)

    if request.method == 'POST':
        form = WorkDayForm(request.POST, instance=WorkDay())
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user = request.user
            if new_log.days == '1':
                new_log.hours = 7.5
            else:
                new_log.hours = 3.75
            new_log.save()
            return HttpResponseRedirect(reverse('view-my-times'))
        else:
            return render(request, 'app/workdayform.html', {'form': form})
    else:
        form = WorkDayForm(initial={'date': datetime.date.today().isoformat()}, instance=WorkDay())
    return render(request, 'app/workdayform.html', {'form': form, 'times': weekly_times})

@login_required(login_url='/user/login/')
def addProject(request):
    if request.method == 'POST':
        form = AddProjectForm(request.POST, instance=Project())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('log-time'))
        else:
            return render(request, 'app/addprojectform.html', {'form': form})
    else:
        form = AddProjectForm(instance=Project())
    return render(request, 'app/addprojectform.html', {'form': form})


@login_required(login_url='/user/login/')
def viewMyTimes(request):
    logged_in_user = request.user
    current_filters = getFilters(request)
    filter_list = Project.objects.all()
    times = WorkDay.objects.filter(user=logged_in_user).order_by('date')

    if times:
        if current_filters['project'] != 'all':
            times = times.filter(project=current_filters['project'])

        if current_filters['date_to'] != '':
            times = times.filter(date__gt=current_filters['date_to'])

        if current_filters['date_from'] != '':
            times = times.filter(date__lt=current_filters['date_from'])

    filters = [{"label": "Project", "name": "project", "options": filter_list}]

    return render(request, 'app/viewmytimes.html', {'times': times, 'filters': filters})


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
    current_filters = getFilters(request)

    if current_filters['project'] != 'all':
        projects = Project.objects.filter(pk=current_filters['project'])
    else:
        projects = Project.objects.all()

    all_projects = {}
    filter_list = Project.objects.all()

    for project in projects:
        times = WorkDay.objects.filter(project=project).order_by('date')
        if times:

            if current_filters['date_from'] != '':
                times = times.filter(date__gte=current_filters['date_from'])

            if current_filters['date_to'] != '':
                times = times.filter(date__lte=current_filters['date_to'])

            sort = request.GET.get('sort', 'none')
            if sort == 'date':
                times = times.order_by('date')
            elif sort == 'user':
                times = times.order_by('user__first_name', 'date')
            total_time = 0
            for time in times:
                total_time += float(time.days)
            all_projects[project.projectName] = {
                'project_id': project.pk,
                'times': times,
                'total_time': total_time,
            }

    filters = [{"label": "Project", "name": "project", "options": filter_list}]

    return render(request, 'app/viewprojects.html', {
                'projects': all_projects,
                'filters': filters,
                'date_to': current_filters['date_to'],
                'date_from': current_filters['date_from']
                })

@login_required(login_url='/user/login/')
def usersView(request):
    user_filter = request.GET.get('user', 'all')
    date_to_filter = request.GET.get('dateto', '')
    date_from_filter = request.GET.get('datefrom', '')

    if user_filter != 'all':
        users = User.objects.filter(pk=user_filter)
    else:
        users = User.objects.order_by('first_name')

    # all_users is a list, so that it can retain the queryset order (rather than dict)
    all_users = []
    filter_list = User.objects.all()

    for user in users:

        times = WorkDay.objects.filter(user=user).order_by('date')

        if date_from_filter != '':
            times = times.filter(date__gte=date_from_filter)

        if date_to_filter != '':
            times = times.filter(date__lte=date_to_filter)

        sort = request.GET.get('sort', 'none')
        if sort == 'date':
            times = times.order_by('date')
        elif sort == 'project':
            times = times.order_by('project__projectName', 'date')

        if user.first_name and user.last_name:
            username = user.first_name + ' ' + user.last_name
        else:
            username = user.username

        all_users.append({username: {"times":times}})

    filters = [{"label": "User", "name": "user", "options": filter_list}]

    return render(request, 'app/viewusers.html', {'users': all_users, 'filters': filters})


@login_required(login_url='/user/login/')
def getProjectCSV(request):
    current_filters = getFilters(request)

    project = Project.objects.get(pk=current_filters['project'])

    times = WorkDay.objects.filter(project=project).order_by('date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + project.projectName + '"'

    if times:

        if current_filters['date_from'] != '':
            times = times.filter(date__gt=current_filters['date_from'])
            response['Content-Disposition'] += "_" + current_filters['date_from']

        if current_filters['date_to'] != '':
            times = times.filter(date__lt=current_filters['date_to'])
            response['Content-Disposition'] += "_" + current_filters['date_to']

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


def getFilters(request):
    project_filter = request.GET.get('project', 'all')
    date_to_filter = request.GET.get('dateto', '')
    date_from_filter = request.GET.get('datefrom', '')

    filters = {
        "project": project_filter,
        "date_to": date_to_filter,
        "date_from": date_from_filter,
    }

    return filters
