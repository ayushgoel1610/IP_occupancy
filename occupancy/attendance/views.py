from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib import auth
import pycurl
import json
import os, csv
import StringIO
import urllib
from datetime import *
import re
# Create your views here.

def curl_request_addr(address,url):
  ### Code to read token from file ###
  module_dir = os.path.dirname(__file__) # get current directory
  file_dir = os.path.join(module_dir,'token')
  handle = open(file_dir,'r')
  auth_token = handle.readline()
  ### END - Code to read token - END ###
  url = urllib.quote(url,safe="%/:=&?~#+!$,;'@()*[]")
  api_data_url = address+url+"&token="+auth_token
  api_data_url = str(api_data_url.encode('utf-8')) # done to fix on server
  print api_data_url
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
  return api_data

def curl_request(url):
  return curl_request_addr("https://192.168.1.40:9199",url)

def last_day_of_month(any_day):
  next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
  return next_month - timedelta(days=next_month.day)

def default_date(month):
  int_month = num(month)
  today = datetime.strptime("01 "+str(int_month)+" 15","%d %m %y")
  return str(today)

def num(month):
  int_month = date.today().month
  try:
    tmp = int(month)
    if tmp >= 1 and tmp <= 12:
      int_month = tmp
  except:
    a = 1
  return int_month

def date_string(month):
  int_month = num(month)
  today = datetime.strptime("01 "+str(int_month)+" 15","%d %m %y")
  first_day = str(today.year)+"-"+str(today.month)+"-01"
  last_day = str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_month(today).day)
  return "&from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"

def index(request):
  month = 1
  dates = []
  p_exceptions = []
  n_exceptions = []
  ta_info_json = {}
  if request.user and request.user.is_authenticated() :
    if request.user.email.split("@")[-1] != 'iiitd.ac.in':
      auth.logout(request)
      template = loader.get_template('attendance/main.html');
      context = RequestContext(request,{'request':request,'user':request.user})
      return HttpResponse(template.render(context));
    month = request.GET.get('m',str(date.today().month))
    api_data_url = "/attendance/get?email="+ str(request.user.email) + date_string(month)
    api_data = curl_request(api_data_url)
    stmt = "/ta/get?email=" + str(request.user.email)
    jdata = json.loads(api_data)
    ta_info_json_str = curl_request(stmt)
    ta_info_json = json.loads(ta_info_json_str)
    for date_iterator in jdata["present_dates"]:
      dates.append(date_iterator)
    print dates
    api_url = "/exceptions/get?" + date_string(month)
    api_data = curl_request(api_url)
    exceptions_j = json.loads(api_data)
    for date_iterator in exceptions_j["positive exceptions"]:
      p_exceptions.append(date_iterator)
    for date_iterator in exceptions_j["negative exceptions"]:
      n_exceptions.append(date_iterator)
    template = loader.get_template('attendance/index.html');
    context = RequestContext(request,{'request':request, 'user': request.user, 'dates':dates,'info':ta_info_json,'positive_exceptions':p_exceptions,'negative_exceptions':n_exceptions,'default_date':default_date(month),'month':num(month)})
  else:
    template = loader.get_template('attendance/main.html');
    context = RequestContext(request,{'request':request,'user':request.user})
  return HttpResponse(template.render(context))
