# Textdrive Server Deployment with Nginx via FastCGI

My notes on deploying a Django application (this website) on Textdrive shared hosting with Nginx via [FastCGI](https://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/).

Thanks to [Evan Carmi](http://ecarmi.org/writing/django-on-joyent/), who much of this is paraphrased from, and [Pokoka](http://tumunu.com/) who has  far more knowledge on system administration than I, and [has an alternate method using uWSGI](http://discuss.textdrive.com/viewtopic.php?id=531).

## Search and Replace

yourusername  
yourdomain.tld  
yourproject  
yourportnumber

## Server folder layout
    :::text
    yourusername
        domains
            yourdomain.tld
                .virtualenv     <- virtual environment
                    yourproject
                        bin
                        include
                        lib
                            python2.7/site-packages     <- where django and packages installed with pip go
                        src
                etc
                    nginx
                        sites-enabled
                            nginx.conf      <- nginx config file (=todo:create symlink from here to web/yourproject/yourproject/conf below)
                web
                    yourproject
                        yourproject     <- django project git repository cloned from github
                        init.sh     <- fcgi startup script. don't forget to make executable with chmod +x init.sh
                        manage.py
                public
                    static   <- static files - either create symlink from here to project repo or run python manage.py collectstatic
                    static/files    <- static files uploaded by users of your app
                    static/@admin    <- django admin media symlink

## SSH into your Txd server
    
    :::bash
    $ ssh yourusername@yourserver.textdrive.us

## Install virtualenv

    :::bash
    $ mkdir -p local/
    $ cd local/
    $ wget -O virtualenv-1.9.1.tar.gz http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz
    $ tar xzvf virtualenv-1.9.1.tar.gz

Let’s now create our virtualenv on our server. This is the same as on our local machine:

    :::bash
    $ python virtualenv.py --no-site-packages ~/domains/yourdomain.tld/.virtualenv/yourproject
    $ cd ~/domains/yourdomain.tld/.virtualenv/yourproject
    $ . bin/activate

## Setup the server’s virtualenv

Create a symbolic link called 'yourproject' in `~/domains/yourdomain.tld/.virtualenv/yourproject/lib/python2.7/site-packages`:

    :::bash
    $ ln -s `pwd` ../lib/python2.7/site-packages/`basename \`pwd\`` 
    $ export DJANGO_SETTINGS_MODULE=yourproject.settings

Add the previous line - `export DJANGO_SETTINGS_MODULE=yourproject.settings` - to the `~/domains/yourdomain.tld/.virtualenv/yourproject/bin/activate` file:

    :::bash
    $ echo "!!" >> ../bin/activate

## Activate virtualenv

    :::bash
    $ source ~/domains/yourdomain.tld/.virtualenv/yourproject/bin/activate

## Install Django, then upload your application to the server

    :::bash
    $ pip install django
    $ cd ~/domains/yourdomain.tld/web/
    $ python django-admin.py startproject yourproject
    
This will have created the following folder layout under `~/domains/yourdomain.tld/web/`:

    :::test
    yourproject
        manage.py
        yourproject     <- default django app

Remove the latter yourproject folder (the default django app created by the startproject command) and replace it with your own project cloned from Github or elsewhere, since, like a good citizien, you are developing locally and only putting tested applications on the production server. Leave manage.py alone.

    :::bash
    $ cd ~/domains/yourdomain.tld/web/yourproject/
    $ rm -rf yourproject
    $ git clone https://github.com/yourusername/yourproject/ yourproject
    Initialized empty Git repository in /users/home/yourusername/domains/yourusername/web/yourproject

[Set up your settings files for production (=TODO: Set up django-configurations)](http://stackoverflow.com/a/88331/412329) and update the database settings to use your PostgreSQL or MySQL database if you are using those instead of sqlite3. If you use PostgreSQL or MySQL you need to create those first in virtualmin.

    :::bash
    DATABASES = { 
        'default': { 
            'ENGINE': 'postgresql_psycopg2', 
            'NAME': 'yourusername_django_mysite_database', 
            'USER': 'yourusername', 
            'PASSWORD': 'password', 
            'HOST': 'localhost', 
            'PORT': '5432', 
        } 
    } 

Try running `python manage.py syncdb`. If it works then your database is configured correctly.

## Install required software packages on the server with pip

Let’s install the software packages from your application's requirements.txt file (if you have one).

    :::bash
    $ cd ~/domains/yourdomain.tld/web/yourproject/yourproject
    $ pip install -r requirements.txt

## Setup static media

Let’s assume you have some static media for your project in `~/domains/yourdomain.tld/web/yourproject/yourproject/static`

For security reasons (but don’t trust me on this) we don’t want to serve static media (CSS, JavaScript, images) from inside our project directory. Instead, let’s create some other directories to serve static media from:

    :::bash
    $ mkdir -p ~/domains/yourdomain.tld/web/public/static

And then create a symbolic link from there to our media directory.

    :::bash
    $ ln -s ~/domains/yourdomain.tld/web/yourproject/yourproject/static/ ~/domains/yourdomain.tld/web/public/static

Now let’s link Django’s contrib.admin media to this location so that the static assets of Django's admin app get served as well:

    :::bash
    $ ln -s ~/domains/yourdomain.tld/.virtualenv/yourproject/lib/python2.7/site-packages/django/contrib/admin/static/admin/ ~/domains/yourdomain.tld/web/yourproject/yourproject/static/admin

And lastly let’s configure settings.py (or settings_local.py depending on your project setup) to use these locations:

    :::python
    import os
    import sys
    
    from os.path import dirname, join
    from sys import path
    
    path.append(join(dirname(__file__), "yourproject"))
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    
    STATIC_URL = 'http://domain.tld/static/'
    ADMIN_MEDIA_PREFIX = os.path.join(PROJECT_ROOT, "admin/")

## Setup NginX and FastCGI

Create a directory to keep your nginx.conf file and the nginx.conf file itself:

    :::bash
    $ mkdir -p ~/yourdomain.tld/etc/nginx/sites-enabled 
    $ vim ~/yourdomain.tld/etc/nginx/sites-enabled/nginx.conf 

**=TODO: keep nginx conf in the project's git repository and create symlink from sites-enabled to yourproject/conf/nginx.conf. This way we can keep the config in version control.**

Edit your nginx.conf file to look like the following but with your own port number[^portnumber] (yourportnumber), domain (yourdomain.tld), and username (yourusername).

    :::nginx
    # http://stackoverflow.com/questions/13371925/how-to-turn-off-or-specify-the-nginx-error-log-location
    error_log /dev/null crit;
    
    worker_processes 1;
    pid /users/home/yourusername/domains/yourdomain.tld/tmp/nginx.pid;
    
    events { 
        worker_connections  24; 
    } 
    
    http { 
        include     /opt/local/etc/nginx/mime.types; 
    
        client_body_temp_path /users/home/yourusername/domains/yourdomain.tld/var/spool/nginx/client_temp 1 2;
        proxy_temp_path /users/home/yourusername/domains/yourdomain.tld/var/spool/nginx/proxy_temp 1 2;
        fastcgi_temp_path /users/home/yourusername/domains/yourdomain.tld/var/spool/nginx/fstcgi_temp 1 2; 
        uwsgi_temp_path /users/home/yourusername/domains/yourdomain.tld/var/spool/nginx/uwsgi_temp 1 2; 
        scgi_temp_path /users/home/yourusername/domains/yourdomain.tld/var/spool/nginx/scgi_temp 1 2; 
    
        log_format main '$remote_addr - $remote_user [$time_local] '
                      '"$request" $status  $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
                  
        access_log /users/home/yourusername/domains/yourdomain.tld/logs/nginx/nginx.access.log;
        error_log /users/home/yourusername/domains/yourdomain.tld/logs/nginx/nginx.error.log;
    
        server { 
            listen       yourportnumber; 
            server_name  yourdomain.tld; 
            # error_log /users/home/yourusername/domains/yourdomain.tld/logs/nginx-fcgi.error.log;
        
            location /static/files  {
                alias /users/home/yourusername/domains/yourdomain.tld/web/public/static/files;
            }
        
            location /static {
                alias /users/home/yourusername/domains/yourdomain.tld/web/public/static;
            }
        
            location / { 
                fastcgi_pass unix:/users/home/yourusername/domains/yourdomain.tld/web/yourproject/yourproject.socket; 
            
                # fastcgi parameters 
                fastcgi_param PATH_INFO $fastcgi_script_name; 
                fastcgi_param QUERY_STRING $query_string; 
                fastcgi_param REQUEST_METHOD $request_method; 
                fastcgi_param SERVER_PORT $server_port; 
                fastcgi_param SERVER_PROTOCOL $server_protocol; 
                fastcgi_param SERVER_NAME $server_name; 
                fastcgi_param CONTENT_TYPE $content_type; 
                fastcgi_param CONTENT_LENGTH $content_length; 
            }    
        }   
    }

Create an init.sh script in your project directory to start the Django FastCGI process that should look like:

    :::bash
    #!/usr/local/bin/bash 
    
    #Activate the virtualenv 
    source /users/home/yourusername/domains/yourdomain.tld/.virtualenv/yourproject/bin/activate
    
    PROJECT_NAME="yourproject"
    PROJECT_DIR="/users/home/yourusername/domains/yourdomain.tld/web/yourproject/yourproject" 
    PID_FILE="/users/home/yourusername/domains/yourdomain.tld/web/yourproject/yourproject.pid" 
    SOCKET_FILE="/users/home/yourusername/domains/yourdomain.tld/web/yourproject/yourproject.socket" 
    BIN_PYTHON="/users/home/yourusername/domains/yourdomain.tld/.virtualenv/yourproject/bin/python" 
    # DJANGO_ADMIN="/users/home/yourusername/domains/yourdomain.tld/.virtualenv/yourproject/bin/django-admin.py" 
    MANAGE="/users/home/yourusername/domains/yourdomain.tld/web/yourproject/manage.py" 
    OPTIONS="maxchildren=2 maxspare=2 minspare=1"
    METHOD="prefork" 
    
    case "$1" in
        start) 
          # Starts the Django process 
          echo "Starting Django project" 
          # $BIN_PYTHON $DJANGO_ADMIN runfcgi $OPTIONS method=$METHOD socket=$SOCKET_FILE pidfile=$PID_FILE 
          $BIN_PYTHON $MANAGE runfcgi $OPTIONS method=$METHOD socket=$SOCKET_FILE pidfile=$PID_FILE 
      ;;  
        stop) 
          # stops the daemon by cating the pidfile 
          echo "Stopping Django project" 
          kill `/bin/cat $PID_FILE` 
      ;;  
        restart) 
          ## Stop the service regardless of whether it was 
          ## running or not, start it again. 
          echo "Restarting process" 
          $0 stop
          $0 start
      ;;  
        *)  
          echo "Usage: init.sh (start|stop|restart)" 
          exit 1
      ;;  
    esac

### Make this init.sh file executable:

    :::bash
    $ chmod +x /users/home/yourusername/domains/yourdomain.tld/web/yourproject/init.sh

### Start Django FastCGI instance with:

    :::bash
    $ /users/home/yourusername/domains/yourdomain.tld/web/yourproject/init.sh start

This script also takes start, stop, and restart as parameters.

### Launch Nginx with your configuration file:

    :::bash
    $ /usr/local/sbin/nginx -p /users/home/yourusername/ -c /users/home/yourusername/domains/yourdomain.tld/etc/nginx/sites-enabled/nginx.conf
    
The Django application should now be running at http://domain.tld:PORTNUBMER/. Don't forget to log in and go to http://domain.tld:yourportnumber/admin/sites/site/ and set the domain name.

## Create a ProxyPath and ProxyPathReverse from http://domain.tld:PORTNUMBER to http://domain.tld

1. Log into your txd account through virtualmin (https://virtualmin-yourserverlocationid.textdrive.us/yourserver/)
2. Under "Server Configuration" click on "Proxy Paths"
3. Click "Add a new proxy path."
4. Enter "/" for the "Local URL path"
5. Enter "http://127.0.0.1:yourportnumber" for the "Destination URL".
6. Click "Save"

ProxyPassReverse:

1. Click "Services"
2. Click "Configure website"
3. Click "Show Directives"
4. From the drop down list chose "ProxyPassReverse"
5. Find the heading "Map remote Location: headers to local"
6. For "Local URL Path" add "/"
7. For "Remote URL" add "balancer://root/"

NOTE: the balancer name should be the same as the one entered for "Remote URL" under "Map local to remote URLs".

<!-- =TODO: Now, in virtualmin create bootup actions to start the Django FastCGI process and NginX on server reboots. -->

## Stopping Nginx

    :::bash
    $ ps -ef | grep nginx | awk '{print $2}'| xargs kill -9

## Stopping fcgi (whenever you update your application you need to stop and then start fcgi)

    :::bash
    $ . init.sh stop

## Todo:

Set up [fabric](http://docs.fabfile.org/) script to automate deployment.

[^portnumber]: To find a free port number you can use for your account, log into your TXD2 account via virtualmin, the click on Other Tools and Check Ports.