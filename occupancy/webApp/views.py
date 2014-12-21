from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from webApp.models import *
from time import strftime
from datetime import *
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
# from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
import pycurl
import json 
import StringIO
import os, csv
import urllib

# Create your views here.

def chart1(request):
 return render(request, 'webApp/home.html')
 	

def chart2(request):
	return render(request, 'webApp/chart2.html')

def last_day_of_month(any_day):
  next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
  return next_month - timedelta(days=next_month.day)

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

def authenticate_user(email):
  if email in ["digvijay09020@iiitd.ac.in","psingh@iiiitd.ac.in","ayush12029@iiitd.ac.in","ashutosh@iiitd.ac.in"]:
    return True
  else:
    return False

def admin_attendance(request):
  Access = 0
  api_data = {}
  if request.user and request.user.is_authenticated() :
    if authenticate_user(request.user.email.lower()):
      today = date.today()
      first_day = str(today.year)+"-"+str(today.month)+"-01"
      last_day = str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_month(today).day)
      stmt = "/attendance/get?from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"
      api_data = curl_request(stmt);
      Access=1
  template = loader.get_template('webApp/attendance.html');
  context = RequestContext(request,{'request':request, 'user': request.user, 'json':api_data,'access':Access})
  return HttpResponse(template.render(context))

def attendance_CSV(request):
	today = date.today()
	today = today -  relativedelta(days = 1)
	last_date = today - relativedelta(days = today.day - 1)
	temp_today = date.today()
	key_dates = []
	list_of_dicts = []
	size = 0
	while(str(last_date)!= str(temp_today)):
		objects = Attendance.objects.filter(date = last_date)
		if (len(objects) > size):
			size = len(objects)
		last_date = last_date + relativedelta(days = 1)
	last_date = today - relativedelta(days = today.day - 1)

	for i in range(size):
		dict = {}
		list_of_dicts.append(dict)
	# print list_of_dicts
	while(str(last_date)!= str(temp_today)):
		key_dates.append(last_date)
		objects = Attendance.objects.filter(date = last_date)
		i = 0
		for o in objects:
			print list_of_dicts[i]
			list_of_dicts[i][last_date] = o.roll_number
			i = i + 1
		last_date = last_date + relativedelta(days = 1)
	response = HttpResponse(content_type = "text/csv")
	response['Content-Disposition'] = 'attachment; filename="TA_Attendance.csv"'
	dict_writer = csv.DictWriter(response, key_dates)
	dict_writer.writer.writerow(key_dates)
	dict_writer.writerows(list_of_dicts)
	return response



def past_week_data(request,time):
	# print time
	current_time = datetime.strptime(time,"%Y-%m-%d-%H:%M:%S")
	current_time= current_time - relativedelta(days = 7)
	# print current_time
	module_dir = os.path.dirname(__file__) # get current directory
	file_dir = os.path.join(module_dir,'token')
	handle = open(file_dir,'r')
	auth_token = handle.readline()
	i = 7
	list = []
	while i>0:
		current_time= current_time + relativedelta(days = 1)
		url_time=current_time.strftime("%Y-%m-%d-%H:%M:%S")
		api_data = curl_request_addr("https://192.168.1.40:9119","/count?at=" + url_time + "&format=yyyy-mm-dd-hh24:mi:ss&type=bfwr")
		api_to_json = json.loads(api_data)
		# count = 0
		for j in range(0,int(api_to_json["size"])):
			dict = {}
			#count = count + int(api_to_json["occupancy_information"][j]["count"])
			dict["day"] = current_time.strftime("%m/%d/%Y")
			dict["building"] = api_to_json["occupancy_information"][j]["building"]
			dict["floor"] = api_to_json["occupancy_information"][j]["floor"]
			dict["wing"] = api_to_json["occupancy_information"][j]["wing"]
			dict["room"] = api_to_json["occupancy_information"][j]["room"]
			dict["count"] = api_to_json["occupancy_information"][j]["count"]
			list.append(dict)
		i = i -1
	keys = ['day','building','floor','wing','room','count']
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="past_week_data.csv"'
	dict_writer = csv.DictWriter(response, keys)
	dict_writer.writer.writerow(keys)
	dict_writer.writerows(list)
	return response

def past_same_day(request, time):
	current_time = datetime.strptime(time,"%Y-%m-%d-%H:%M:%S")
	current_time= current_time - relativedelta(days = 42)
	module_dir = os.path.dirname(__file__) # get current directory
	file_dir = os.path.join(module_dir,'token')
	handle = open(file_dir,'r')
	auth_token = handle.readline()
	i = 7
	list = []
	while i>0:
		url_time=current_time.strftime("%Y-%m-%d-%H:%M:%S")
		api_data = curl_request_addr("https://192.168.1.40:9119","/count?at=" + url_time + "&format=yyyy-mm-dd-hh24:mi:ss&type=bfwr")
		api_to_json = json.loads(api_data)
		for j in range(0,int(api_to_json["size"])):
			dict = {}
			#count = count + int(api_to_json["occupancy_information"][j]["count"])
			dict["day"] = current_time.strftime("%m/%d/%Y")
			dict["building"] = api_to_json["occupancy_information"][j]["building"]
			dict["floor"] = api_to_json["occupancy_information"][j]["floor"]
			dict["wing"] = api_to_json["occupancy_information"][j]["wing"]
			dict["room"] = api_to_json["occupancy_information"][j]["room"]
			dict["count"] = api_to_json["occupancy_information"][j]["count"]
			list.append(dict)
		current_time = current_time + relativedelta(days= 7)
		i = i -1
	keys = ['day','building','floor','wing','room','count']
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="past_same_day.csv"'
	dict_writer = csv.DictWriter(response, keys)
	dict_writer.writer.writerow(keys)
	dict_writer.writerows(list)
	return response

def month_average(request, time):
	current_time = datetime.strptime(time,"%Y-%m-%d-%H:%M:%S")
	current_time = current_time - relativedelta(days = 30, minutes=current_time.minute)
	module_dir = os.path.dirname(__file__) # get current directory
	file_dir = os.path.join(module_dir,'token')
	handle = open(file_dir,'r')
	auth_token = handle.readline()
	i=30
	list = []
	temp_array = ["Academic","Boy's Hostel","Girl's Hostel","Library","Residence","Service Block","Student Centre"]
	key_index = {"Academic":"Acad","Boy's Hostel":"BH","Girl's Hostel":"GH","Library":"L","Residence":"R","Service Block":"SB","Student Centre":"SC"}
	while(i>=0):
		temp_time = current_time + relativedelta(days = 30 - i,minutes = 15)
		j=0
		count = []
		count[0:7] = [0,0,0,0,0,0,0]
		for j in range(0,2):
			url_time=temp_time.strftime("%Y-%m-%d-%H:%M:%S")
			api_data = curl_request_addr("https://192.168.1.40:9119","/count?at=" + url_time + "&format=yyyy-mm-dd-hh24:mi:ss&type=bfwr")
			api_to_json = json.loads(api_data)
			# print api_to_json["occupancy_information"][0]["count"]
			for k in range(0,int(api_to_json["size"])):
				index = temp_array.index(api_to_json["occupancy_information"][k]["building"])
				count[index] = count[index] + int(api_to_json["occupancy_information"][k]["count"])
			temp_time = temp_time + relativedelta(minutes = 30)
		temp_time = temp_time - relativedelta(minutes = 75)
		dict = {}
		dict["day"] = temp_time
		for j in range(0,int(api_to_json["size"])):
			index = temp_array.index(api_to_json["occupancy_information"][j]["building"])
			dict[key_index[api_to_json["occupancy_information"][j]["building"]]] = count[index]/2
		list.append(dict)
		i=i-1
	keys = ["day","Acad","BH","GH","L","R","SB","SC"]
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="month_average.csv"'
	dict_writer = csv.DictWriter(response, keys)
	dict_writer.writer.writerow(keys)
	dict_writer.writerows(list)
	return response

# def try1(request):
# 	module_dir = os.path.dirname(__file__)
# 	file_dir = os.path.join(module_dir,'token')
# 	handle = open(file_dir,'r')
# 	auth_token = handle.readline()
# 	i = 60
# 	time = date.today()
# 	time = time.strftime("%Y-%m-%d-%H:%M:%S")
# 	print "entered"
# 	while(i>=0):
# 		api_data_url = "https://192.168.1.40:9119/count?at=" + time + "&format=yyyy-mm-dd-hh24:mi:ss&type=b&token="+auth_token
# 		c = pycurl.Curl()
# 		c.setopt(pycurl.URL, api_data_url)
# 		c.setopt(pycurl.SSL_VERIFYPEER, 0)
# 		c.setopt(pycurl.SSL_VERIFYHOST, 0)
# 		b = StringIO.StringIO()
# 		c.setopt(pycurl.WRITEFUNCTION, b.write)
# 		c.setopt(pycurl.FOLLOWLOCATION, 1)
# 		c.setopt(pycurl.MAXREDIRS, 5)
# 		c.perform()
# 		api_data = b.getvalue()
# 		api_to_json = json.loads(api_data)
# 		i = i - 1
# 		print i
# 	print "done"
# 	return HttpResponse("done")

def admin_students(request):
  api_data={}
  Access = 0
  if request.user and request.user.is_authenticated() :
    if authenticate_user(request.user.email.lower()):
      api_data_url = "/ta/get?"
      api_data = curl_request(api_data_url)
      Access = 1
  template = loader.get_template('webApp/admin_students.html');
  context = RequestContext(request,{'request':request, 'user': request.user, 'json':api_data,'access':Access})
  return HttpResponse(template.render(context))

def admin_insert_ta(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        batch = request.POST.get('batch')
        name = request.POST.get('name')
        stmt = "/ta/put?rollno="+rollno+"&email="+email+"&batch="+batch+"&name="+name
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_modify_attendance(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        date = request.POST.get('date')
        option = request.POST.get('set-options')
        stmt = "/attendance/put?rollno="+rollno+"&at="+date+"&format=yyyy-mm-dd&present="+option
        api_data = curl_request(stmt)
        print request.POST
        return HttpResponseRedirect("/template/admin/")
  return HttpResponse("HelloWorld")

#Nothing
def admin_insert(request, ta, mac):
	test = Admin.objects.filter(TA = ta)
	if not test:
		TA_object = Admin(TA = ta, mac = mac, deleted = 0)
		TA_object.save()
	else:
		test.delete()
		TA_object = Admin(TA = ta, mac = mac, deleted = 0)
		TA_object.save()

	return HttpResponseRedirect('/template/admin/')
	# return HttpResponse("ayush")

def admin_delete(request, ta):
	del_object = Admin.objects.filter(TA = ta)
	del_object.update(deleted = 1)
	return HttpResponseRedirect('/template/admin/')
