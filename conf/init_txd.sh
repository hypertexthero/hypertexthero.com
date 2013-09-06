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