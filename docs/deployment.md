# hypertexthero.com Server Deployment with Nginx via [FastCGI](https://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/)

Thanks to [Evan Carmi](http://ecarmi.org/writing/django-on-joyent/) and [Poko](http://tumunu.com/).

## Server folder layout

    sgriffee
        domains
            hypertexthero.com
                .virtualenv     <- virtual environment
                    hth
                        bin
                        include
                        lib
                        src
                etc
                    nginx
                        sites-enabled
                            nginx.conf      <- nginx config file (=todo:create symlink from here to web/hth/hth/conf below)
                web
                    hth
                        hth     <- django project git repository cloned from github
                        init.sh     <- fcgi startup script. don't forget to make executable with chmod +x init.sh
                        manage.py
                public
                    static   <- static files - either create symlink from here to project repo or run python manage.py collectstatic
                    static/files    <- static files uploaded by users of your app
                    static/@admin    <- admin media symlink

## Setup the server’s virtualenv

create a symbolic link called 'hth' in ~/domains/hypertexthero.com/.virtualenv/hth/lib/python2.7/site-packages

    $ ln -s `pwd` ../lib/python2.7/site-packages/`basename \`pwd\`` 
    $ export DJANGO_SETTINGS_MODULE=hth.settings

add previous line - export DJANGO_SETTINGS_MODULE=hth.settings - ~/domains/hypertexthero.com/.virtualenv/hth/bin/activate file

    $ echo "!!" >> ../bin/activate

## Activate virtualenv

source ~/domains/hypertexthero.com/.virtualenv/hth/bin/activate

## Install packages on the server with pip

Let’s install the packages in our REQUIREMENTS file.

    $ pip install -r REQUIREMENTS

## Setup static media

Let’s assume you have some static media for your project in `~/domains/hypertexthero.com/web/hth/hth/static`

For security reasons (but don’t trust me on this) we don’t want to serve static media (CSS, Javacsript) from inside our project directory. Instead, let’s create some other directories to serve static media from:

    $ mkdir -p ~/domains/hypertexthero.com/web/public/static

And then create a symbolic link from there to our media directory.

    $ ln -s ~/domains/hypertexthero.com/web/hth/hth/static/ ~/domains/hypertexthero.com/web/public/static

Now let’s link Django’s contrib.admin media to this location:

    $ ln -s ~/domains/hypertexthero.com/.virtualenv/hth/lib/python2.7/site-packages/django/contrib/admin/static/admin/ ~/domains/hypertexthero.com/web/hth/hth/static/admin

And lastly let’s configure our settings.py to use these locations:

    import os
    import sys
    
    from os.path import dirname, join
    from sys import path
    
    path.append(join(dirname(__file__), "hth"))
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    
    STATIC_URL = 'http://domain.tld/static/'
    ADMIN_MEDIA_PREFIX = os.path.join(PROJECT_ROOT, "admin/")

## Setup NginX and FastCGI

Now let’s get NginX running.

Create a nginx.conf file inside your site directory:

**=TODO: keep nginx conf in project git repository and create symlink from sites-enabled to hth/conf/nginx.conf**

    $ mkdir -p ~/hypertexthero.com/etc/nginx/sites-enabled 
    $ vim ~/hypertexthero.com/etc/nginx/sites-enabled/nginx.conf 

Edit your nginx.conf file to look like the following but with your own port number, domain, and username. In the example my port is 11180, my domain is hypertexthero.com, and my username is sgriffee:

    # http://stackoverflow.com/questions/13371925/how-to-turn-off-or-specify-the-nginx-error-log-location
    error_log /dev/null crit;
    
    worker_processes 1;
    pid /users/home/sgriffee/domains/hypertexthero.com/tmp/nginx.pid;
    
    events { 
        worker_connections  24; 
    } 
    
    http { 
        include     /opt/local/etc/nginx/mime.types; 
    
        client_body_temp_path /users/home/sgriffee/domains/hypertexthero.com/var/spool/nginx/client_temp 1 2;
        proxy_temp_path /users/home/sgriffee/domains/hypertexthero.com/var/spool/nginx/proxy_temp 1 2;
        fastcgi_temp_path /users/home/sgriffee/domains/hypertexthero.com/var/spool/nginx/fstcgi_temp 1 2; 
        uwsgi_temp_path /users/home/sgriffee/domains/hypertexthero.com/var/spool/nginx/uwsgi_temp 1 2; 
        scgi_temp_path /users/home/sgriffee/domains/hypertexthero.com/var/spool/nginx/scgi_temp 1 2; 
    
        log_format main '$remote_addr - $remote_user [$time_local] '
                      '"$request" $status  $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
                  
        access_log /users/home/sgriffee/domains/hypertexthero.com/logs/nginx/nginx.access.log;
        error_log /users/home/sgriffee/domains/hypertexthero.com/logs/nginx/nginx.error.log;
    
        server { 
            listen       11180; 
            server_name  hypertexthero.com; 
            # error_log /users/home/sgriffee/domains/hypertexthero.com/logs/nginx-fcgi.error.log;
        
            location /static/files  {
                alias /users/home/sgriffee/domains/hypertexthero.com/web/public/static/files;
            }
        
            location /static {
                alias /users/home/sgriffee/domains/hypertexthero.com/web/public/static;
            }
        
            location /typography {
                alias /users/home/sgriffee/domains/hypertexthero.com/web/public/typography;
            }
        
            location /ippc {
                alias /users/home/sgriffee/domains/hypertexthero.com/web/public/ippc;
            }
        
            location / { 
                fastcgi_pass unix:/users/home/sgriffee/domains/hypertexthero.com/web/hth/hth.socket; 
            
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

    #!/usr/local/bin/bash 
    
    #Activate the virtualenv 
    source /users/home/sgriffee/domains/hypertexthero.com/.virtualenv/hth/bin/activate
    
    PROJECT_NAME="hth"
    PROJECT_DIR="/users/home/sgriffee/domains/hypertexthero.com/web/hth/hth" 
    PID_FILE="/users/home/sgriffee/domains/hypertexthero.com/web/hth/hth.pid" 
    SOCKET_FILE="/users/home/sgriffee/domains/hypertexthero.com/web/hth/hth.socket" 
    BIN_PYTHON="/users/home/sgriffee/domains/hypertexthero.com/.virtualenv/hth/bin/python" 
    # DJANGO_ADMIN="/users/home/sgriffee/domains/hypertexthero.com/.virtualenv/hth/bin/django-admin.py" 
    MANAGE="/users/home/sgriffee/domains/hypertexthero.com/web/hth/manage.py" 
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

## Make this init.sh file executable:

    $ chmod +x /users/home/sgriffee/domains/hypertexthero.com/web/hth/init.sh

## Start Django FastCGI instance with:

    $ /users/home/sgriffee/domains/hypertexthero.com/web/hth/init.sh start

This script also takes start, stop, and restart as parameters.

## Launch Nginx with your configuration file:

    $ /usr/local/sbin/nginx -p /users/home/sgriffee/ -c /users/home/sgriffee/domains/hypertexthero.com/etc/nginx/sites-enabled/nginx.conf
    
We should now having our Django application running. Go to http://domain.tld:PORTNUBMER/ to see it. For my app, we can login to the admin interface by going to: http://domain.tld:11180/admin/

**=TODO**: 
**ProxyPath from http://domain.tld:PORTNUMBER TO http://domain.tld**
**ProxyPathReverse from http://domain.tld:PORTNUMBER TO http://domain.tld**

Now, in virtualmin create bootup actions to start the Django FastCGI process and NginX on server reboots.

## kill nginx

ps -ef | grep nginx | awk '{print $2}'| xargs kill -9

## kill fcgi

. init.sh stop