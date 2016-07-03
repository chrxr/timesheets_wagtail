## Timesheet application

This is a Django 1.8 application to manage the recording of developer time on projects.

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

### Deploying repo to production

* In fabfile.py, replace the username in 'bodl2685@timesheets-qa.bodleian.ox.ac.uk' with your own Connect username
* `fab deploy` (whilst in the virtualenv, from the directory containing the fab file)

### Application notes

* Application currently deployed on RHEL 6.7, for which the local python version is 2.6.
* Django requires at least v2.7.
* Python 2.7 is compiled in the bodl2685 home folder (/home/bodl2685/python/).
* Currently running on Apache.
* mod_wsgi also needed to be recompiled, pointing to the appropriate python version and pythonlib files.

### Instructions for recompiling mod_uwsgi pointing to Python 2.7.

    curl -O https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/modwsgi/mod_wsgi-3.4.tar.gz
    tar xvfz mod_wsgi-3.4.tar.gz
    cd mod_wsgi-3.4
    ./configure --with-python=/home/bodl2685/python/2.7.10/bin/python
    LD_RUN_PATH=~/python/2.7.10/lib make
    sudo make install

### Definition of up

* Postgres running
* Apache httpd running
* Timesheets homepage visible at timesheets-qa.bodleian.ox.ac.uk
