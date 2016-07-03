## Timesheet application

This is a Django application to manage the recording of developer time on projects.

### Creating a local build

* `pip install virtualenv`
* `virtualenv timesheets-app`
* `cd timesheets-app`
* `git clone git@github.com:chrxr/timesheets.git`
* `source bin/activate`
* `cd timesheets`
* `createdb timesheets`
* `./manage.py migrate`
* `./manage.py createsuperuser`
* `./manage.py runserver`
