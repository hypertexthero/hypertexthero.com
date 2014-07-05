# Deployment notes

## Software Stack

The deployed stack for <http://hypertexthero.com> consists of the following components running on webfaction:

- [NGINX](http://nginx.org/en/) - public facing web server - serves media and proxies dynamic requests to Gunicorn. Currently using webfactions system-wide nginx.
- [Gunicorn](http://gunicorn.org/ "Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.") - internal HTTP application server
- [sqlite](https://www.sqlite.org/) - database
- [Django](http://djangoproject.com/) web application in Git repository

## Restarting Server After Updates {#restart}

**Note that we will eventually have a [Fabric](http://docs.fabfile.org/en/1.6/) script that will do all of the below with one command. =TODO: Set up Fabric deployment script.**

1. Login to webfaction via SSH

2. Change to the hypertexthero project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/hypertexthero/hypertexthero-env/ && . bin/activate && cd hth

3. Find out the number of the Gunicorn process:

        ps aux | grep gunicorn

4. Kill the process gracefully (replace #### with the number from the output above):

        kill -HUP ####

5. If necessary, restart the Gunicorn server:

        python manage.py run_gunicorn --daemon -b 127.0.0.1:23035 -w 2 --max-requests 500


## Deploying Code

1. Login to webfaction via SSH

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/hypertexthero/hypertexthero-env/ && . bin/activate && cd hth

3. Pull changes from the Github repository master branch:

        git pull origin master

4. Collect static files to static directories in case you changed CSS, JavaScript, site design images, etc (say 'yes' when it asks to overwrite):

        python manage.py collectstatic

5. If you changed Python code, you need to <a href="#restart">restart</a> the server, too. If you only changed code in templates, there is no need to restart. =TODO: Add migration instructions in case we are changing data models.

## Reverting to Previous Commit in Case You Break Something

1. Login to webfaction via SSH

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/hypertexthero/hypertexthero-env/ && . bin/activate && cd hth

3. [Find the hash of the previous commit in your repository](http://git-scm.com/book/en/Git-Basics-Viewing-the-Commit-History):

        git log

4. Checkout previous commit from [the Github repository master branch](https://github.com/hypertexthero/hypertexthero.com/commits/master) using [these instructions](http://stackoverflow.com/a/4114122/412329) or the command below:

         git reset --hard HashOfPreviousCommitHereLotsOfNumberAndLetters

5. [Restart server](#restart)

# Cron (or better yet, supervisord -- see below)

This is the cron job to make sure gunicorn is running.
ssh into webfaction account, type ‘crontab -e’ to edit the cron file and append the following to the bottom of the file:

  30 * * * * cd ~/webapps/hypertexthero/hypertexthero-env/ && /webapps/hypertexthero/hypertexthero-env/bin/python /webapps/hypertexthero/hypertexthero-env/hth/manage.py run_gunicorn --daemon -b 127.0.0.1:23035 -w 2 --max-requests 500


# Supervisord
**Problem:** Your server machine crashes and your website running under an application server such as [Gunicorn](http://gunicorn.org/) goes down. The app server needs to be restarted.

**Solution:** Use [supervisord](http://supervisord.org/) to monitor your application server process and restart it if it dies.

1. Install supervisord:

        pip install supervisor

2. Put the follosing in `~/etc/supervisord.conf` (includes examples for [hypertexthero.com](http://hypertexthero.com) and [Food News](http://food.hypertexthero.com)):

        [unix_http_server]
        file=/home/hth/tmp/supervisor.sock

        [supervisord]
        logfile=/home/hth/logs/user/supervisord.log
        logfile_maxbytes=25MB
        logfile_backups=10
        loglevel=info
        pidfile=/home/hth/etc/supervisord.pid

        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

        [supervisorctl]
        serverurl=unix:///home/hth/tmp/supervisor.sock

        [include]
        files = /home/hth/webapps/hypertexthero/hypertexthero-env/hth/hth/conf/supervisor.ini /home/hth/webapps/foodnews/fn-env/fn/supervisor.ini 

3. Create a `supervisor.ini` file in each web application's repository so we keep supervisor settings for the application in version control. Example:

        [program:hypertexthero.com]
        command=/home/hth/webapps/hypertexthero/hypertexthero-env/bin/python2.7 /home/hth/webapps/hypertexthero/hypertexthero-env/bin/gunicorn_django --daemon -b 127.0.0.1:23035 -w 2 --max-requests 500
        directory=/home/hth/webapps/hypertexthero/hypertexthero-env/hth/hth
        user=hth
        autostart=true
        autorestart=true
        redirect_stderr=True

4. Start supervisord using its main configuration file:

        supervisord -c /home/hth/etc/supervisord.conf

If problem, see [this](http://serverfault.com/a/397970).