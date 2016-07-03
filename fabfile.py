from __future__ import with_statement
from fabric.api import *
from fabric.colors import red


env.roledefs['production'] = ['bodl2685@timesheets-qa.bodleian.ox.ac.uk']

@roles('production')
def deploy_production(branch="master"):
    with cd('/home/bodl2685/timesheets'):
        run("git fetch")
        run("git checkout %s" % branch)
        run("git pull")
        run("/home/bodl2685/timesheets/bin/pip install -r requirements.txt")
        run("/home/bodl2685/timesheets/bin/python manage.py migrate --settings=timesheets.settings.production --noinput")
        run("/home/bodl2685/timesheets/bin/python manage.py collectstatic --settings=timesheets.settings.production --noinput")

        sudo("service httpd restart")

def deploy():
    execute(deploy_production)
