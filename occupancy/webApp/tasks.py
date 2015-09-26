from celery import task
import os
import pycurl
import urllib
import StringIO

def curl_request_addr(address,url):
  ### Code to read token from file ###
  module_dir = os.path.dirname(__file__) # get current directory
  file_dir = os.path.join(module_dir,'token')
  handle = open(file_dir,'r')
  auth_token = handle.readline()
  ### END - Code to read token - END ###
  url = urllib.quote(url,safe="%/:=&?~#+!$,;'@()*[]")
  api_data_url = address+url+"&token="+auth_token
  api_data_url = str(api_data_url.encode('ascii','ignore')) # done to fix random hex charcaters in input string
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

@task()
def update_attendance(url):
  return curl_request(url)
