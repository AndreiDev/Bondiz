#!/home/andreii1/python/bin/python
import sys, os
 
# Add a custom Python path.
sys.path.insert(0, "/home/andreii1/python")
sys.path.insert(13, "/home/andreii1/django_projects/Bondiz")
 
# Switch to the directory of your project. (Optional.)
os.chdir("/home/andreii1/django_projects/Bondiz")
 
# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "Bondiz.settings"
 
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
