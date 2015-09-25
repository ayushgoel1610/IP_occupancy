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

def authenticate_user(email):
  if email in ["digvijay09020@iiitd.ac.in","psingh@iiitd.ac.in","ayush12029@iiitd.ac.in","ashutosh@iiitd.ac.in","anshu@iiitd.ac.in","priti@iiitd.ac.in"]:
    return True
  else:
    return False

def admin_attendance(request):
  Access = 0
  api_data = {}
  holidays=[]
  working_days=[]
  if request.user and request.user.is_authenticated() :
    if authenticate_user(request.user.email.lower()):
      today = date.today()
      first_day = str(today.year)+"-"+str(today.month)+"-01"
      last_day = str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_month(today).day)
      stmt = "/attendance/get?from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"
      api_data = curl_request(stmt)
      stmt2 = "/exceptions/get?from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"
      exceptions_data = json.loads(curl_request(stmt2))
      holidays = exceptions_data["positive exceptions"]
      working_days = exceptions_data["negative exceptions"]
      Access=1
  template = loader.get_template('webApp/attendance.html');
  context = RequestContext(request,{'request':request, 'user': request.user, 'json':api_data,'access':Access,'holidays':holidays,'working_days':working_days})
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

def valid_column_names(column_names):
  # These are the absolute core required names
  valid_names = ['roll no.','name','email id','batch']
  for valid_name in valid_names:
    if valid_name not in column_names:
      return False
  return True

def valid_csv(data):
  # Gets number of columns in first line.
  # All lines should contain same number of columns :)
  csv_lines = data.splitlines()
  column_names = csv_lines[0].split(',')
  column_names = [name.lower().strip() for name in column_names]
  if not valid_column_names(column_names):
    return False
  return True

def extract_indices(data):
 # returns a map of 'column name' to index
 line = data.splitlines()[0]
 indice = {}
 i=0; # iterator
 for column_name in line.split(','):
   indice[column_name.lower().strip()] = i
   i = i + 1
 return indice

def get_student_info(data,indice):
  firstLine = True
  all_students_info = []
  for line in data.splitlines():
    if firstLine :
      firstLine = False
      continue
    student_info = {}
    words = line.split(',')
    for column_names in indice.keys():
      tmp = words[indice[column_names]]
      tmp = unicode(tmp,"utf-8",errors ="ignore")
      student_info[column_names] = tmp.encode('ascii','ignore').strip()
    all_students_info.append(student_info)
  return all_students_info

def push_student_info(all_student_info,request):
  for student_info in all_student_info:
    if student_info['roll no.'] == '':
      continue
    stmt = "/ta/put?rollno="+student_info['roll no.']+"&email="+student_info['email id']+"&batch="+student_info['batch']+"&name="+student_info['name']+"&username="+request.user.email.lower()
    print stmt
    api_data = curl_request(stmt)

def push_student_macs(all_student_info,request):
  for student_info in all_student_info:
    count = 1
    for i in range(len(student_info.keys())):
      device_string = 'device '+str(count)
      if device_string in student_info.keys():
        stmt = "/ta/put?rollno="+student_info['roll no.']+"&mac="+student_info[device_string]+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        count = count + 1
      else:
        break # last device string not found. No point in looking for more

def admin_insert_ta_csv(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        data = request.FILES['upload-file'].read()
        #perform validity check for csv file
        if valid_csv(data):
          indice = extract_indices(data)
          all_student_info = get_student_info(data,indice)
          #loop over student info row by row, first creating new students
          push_student_info(all_student_info,request)
          #loop over file row by row, 'put_mac'ing all the macs
          push_student_macs(all_student_info,request)
          #done!
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_insert_ta(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        batch = request.POST.get('batch')
        name = request.POST.get('name')
        print rollno
        stmt = "/ta/put?rollno="+rollno+"&email="+email+"&batch="+batch+"&name="+name+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_delete_ta(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        print rollno
        stmt = "/ta/del?rollno="+rollno+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_del_mac(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        mac = request.POST.get('mac')
        stmt = "/ta/del?rollno="+rollno+"&mac="+mac+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")


def admin_add_mac(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
	rollno = str(rollno.encode('ascii','ignore'))
	rollno = unicode(rollno,"utf-8",errors="ignore")
        mac = request.POST.get('mac')
	mac = str(mac.encode('ascii','ignore'))
        mac = unicode(mac,"utf-8",errors="ignore")
        stmt = "/ta/put?rollno="+rollno+"&mac="+mac+"&username="+request.user.email.lower()
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
        stmt = "/attendance/put?rollno="+rollno+"&at="+date+"&format=yyyy-mm-dd&present="+option+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        print request.POST
        return HttpResponseRedirect("/template/admin/")
  return HttpResponse("HelloWorld")

def generate_attendance_csv(first_date,last_date,api_data):
  delta = last_date - first_date
  api_to_json = json.loads(api_data)
  attendance =[]
  column_names=['rollno','batch']
  for i in range (delta.days + 1):
    iter_date = first_date + timedelta(days=i)
    if iter_date.weekday() < 5:
      str_date = (first_date + timedelta(days=i)).strftime('%Y-%m-%d')
      column_names.append(str_date)
  attendance.append(column_names)
  for json_student_attendance in api_to_json["attendance"]:
    student_attendance = []
    student_attendance.append(json_student_attendance["rollno"])
    student_attendance.append(json_student_attendance["batch"])
    for i in range (delta.days + 1): #Inefficient. Can be done O(k) where k is the number present dates. RIght now it is in O(nk) where n is the number of dates
      str_date = (first_date + timedelta(days=i)).strftime('%Y-%m-%d')
      iter_date = first_date + timedelta(days=i)
      if iter_date.weekday() < 5:
        if str_date in json_student_attendance["present_dates"]:
          student_attendance.append('P')
        else:
          student_attendance.append('A')
    attendance.append(student_attendance)
  response = HttpResponse(content_type = "text/csv")
  response['Content-Disposition'] = 'attachment; filename="TA_Attendance.csv"'
  csv_writer = csv.writer(response)
  csv_writer.writerows(attendance)
  return response

def admin_add_exception(request):
  print "here111\n"
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      print "here"
      if request.method=='POST':
        date = request.POST.get('date')
        option = request.POST.get('set-options')
        stmt = "/exception/put?at="+date+"&format=yyyy-mm-dd&type="+option+"&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/")
  return HttpResponse("HelloWorld")

def admin_del_exception(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        date = request.POST.get('date')
        option = request.POST.get('set-options')
        stmt = "/exception/del?at="+date+"&format=yyyy-mm-dd&username="+request.user.email.lower()
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/")
  return HttpResponse("HelloWorld")

def admin_download_attendance(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        month = request.POST.get('month')
        first_date_str = month+'-01'
        first_date = datetime.strptime(first_date_str,"%Y-%m-%d")
        last_date_str = month + '-'+ str(last_day_of_month(first_date).day)
        last_date = datetime.strptime(last_date_str,"%Y-%m-%d")
        stmt = "/attendance/get?from="+first_date_str+"&to="+last_date_str+"&format=yyyy-mm-dd"
        api_data = curl_request(stmt)
        response = generate_attendance_csv(first_date,last_date,api_data)
        return response
  return HttpResponse("HelloWorld")

def logs_table(api_data):
  html = "<HTML><BODY><table style=\"border:1px solid grey;width:100%;text-align:left;\">"
  json_api_data = json.loads(api_data)
  print api_data
  html+="<tr>"
  html+="<th>Timestamp</th><th>Action</th><th>User</th>"
  html+="<th>Arguments</th>"
  html+="</tr>"
  for log in json_api_data["logs"]:
    html += "<tr>"
    html += "<td>"+log["ts"]+"</td><td>"+log["action"]+"</td><td>"
    html += log["email"]+"</td><td>"+log["arguments"]+"<td>"
    html += "</tr>"
  html += "</BODY></HTML>"
  return html


def admin_logs_view(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      today = date.today()
      first_day = str(today.year)+"-"+str(today.month)+"-01"
      last_day = str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_month(today).day)
      stmt = "/logs/get?from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"
      api_data = json.loads(curl_request(stmt))["logs"]
      template = loader.get_template('webApp/log.html');
      context = RequestContext(request,{'request':request, 'user': request.user, 'json':api_data})
      return HttpResponse(template.render(context))
  return HttpResponse('Hello World')

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

def error_page(message):
  return HttpResponse(message)

def date_string(month):
  int_month = num(month)
  today = datetime.strptime("01 "+str(int_month)+" 15","%d %m %y")
  first_day = str(today.year)+"-"+str(today.month)+"-01"
  last_day = str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_month(today).day)
  return "&from="+first_day+"&to="+last_day+"&format=yyyy-mm-dd"

def admin_calendar_view(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      p_exceptions =[]
      n_exceptions = []
      month = request.GET.get('m',str(date.today().month))
      api_url = "/exceptions/get?" + date_string(month)
      api_data = curl_request(api_url)
      exceptions_j = json.loads(api_data)
      for date_iterator in exceptions_j["positive exceptions"]:
        p_exceptions.append(date_iterator)
      for date_iterator in exceptions_j["negative exceptions"]:
        n_exceptions.append(date_iterator)
      template = loader.get_template('webApp/calendar.html');
      context = RequestContext(request,{'request':request, 'user': request.user,'positive_exceptions':p_exceptions,'negative_exceptions':n_exceptions,'default_date':default_date(month),'month':num(month)})
      return HttpResponse(template.render(context))
  return error_page('Hello World')

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
