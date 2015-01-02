from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import pycurl
import json
import os, csv
import StringIO
# Create your views here.

def index(request):
  dates = []
  if request.user and request.user.is_authenticated() :
    ### Code to read token from file ###
    module_dir = os.path.dirname(__file__) # get current directory
    file_dir = os.path.join(module_dir,'token')
    handle = open(file_dir,'r')
    auth_token = handle.readline()
    ### END - Code to read token - END ###
    api_data_url = "https://192.168.1.40:9119/attendance?email="+ str(request.user.email) + "&from=2015-01-01&to=2015-01-31&format=yyyy-mm-dd&token="+ auth_token
    c = pycurl.Curl()
    c.setopt(pycurl.URL, api_data_url)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    api_data = b.getvalue()
    print api_data
    jdata = json.loads(api_data)
    for date_iterator in jdata["attendance"]:
      dates.append(date_iterator["date"])
    print dates
  template = loader.get_template('attendance/index.html');
  context = RequestContext(request,{'request':request, 'user': request.user, 'dates':dates})
  return HttpResponse(template.render(context))
