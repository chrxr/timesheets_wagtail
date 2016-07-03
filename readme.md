## Timesheet application

This is a Django application to manage the recording of developer time on projects.

### Dependencies

* Python 2.7+
* Postgres

### Creating a local build

* `pip install virtualenv`
* `virtualenv timesheets-app`
* `cd timesheets-app`
* `git clone git@github.com:chrxr/timesheets.git`
* `source bin/activate`
* `cd timesheets`
* `pip install -r requirements.txt`
* `createdb timesheets`
* `./manage.py migrate`
* `./manage.py createsuperuser`
* `./manage.py runserver`

### Deploying changes

* In fabfile.py, replace the username in 'bodl2685@timesheets-qa.bodleian.ox.ac.uk' with your own Connect username
* `fab deploy` (whilst in the virtualenv, from the project root i.e. timesheets-app/timesheets)
