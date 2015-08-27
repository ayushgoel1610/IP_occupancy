from django.shortcuts import render, render_to_response
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

def chart3(request):
  return render(request, 'webApp/classAttendance.html')

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
  # c.setopt(pycurl.VERBOSE, 1)
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
  if email in ["digvijay09020@iiitd.ac.in","psingh@iiitd.ac.in","ayush12029@iiitd.ac.in","ashutosh@iiitd.ac.in","anshu@iiitd.ac.in","shubham12101@iiitd.ac.in"]:
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
      api_data = curl_request(stmt)
      Access=1
  template = loader.get_template('webApp/attendance.html')
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

def get_avg_count(time, classRoom):
  datetime_now = datetime.now()
  datetime_start = datetime.strptime(time[0],"%Y-%m-%d-%H:%M:%S") 
  numOfWeeks = (((datetime_now-datetime_start).days)/7)+1
  ctr=0
  avgArr = {}
  if(len(time)==2):
    minutes=45
  elif (len(time)==3):
    minutes=30
  elif (len(time)==3):
    minutes=90
  for i in range(0,numOfWeeks):
    total = 0
    ctr=0
    for j in range(0,len(time)):
      newTime = time[j]
      current_time = datetime.strptime(newTime,"%Y-%m-%d-%H:%M:%S") 
      current_time = current_time+relativedelta(minutes=minutes)
      week = current_time + relativedelta(weeks = i)
      url_time=week.strftime("%Y-%m-%d-%H:%M:%S")
      api_data = curl_request_addr("https://192.168.1.40:9119","/count?at=" + url_time + "&format=yyyy-mm-dd-hh24:mi:ss&type=bfwr")
      api_to_json = json.loads(api_data)
      for j in range(0,int(api_to_json["size"])):
        if(api_to_json["occupancy_information"][j]["room"]==classRoom):
          count = int(api_to_json["occupancy_information"][j]["count"])
          total = total+count
          ctr = ctr + 1
      # print "i: ",i," total: ",total, " ctr: ",ctr
      if(ctr>0):
        avgArr["Week"+ str(i+1)] = (total/ctr)
      else:
        avgArr["Week"+ str(i+1)] = 0
  return avgArr

def get_line_chart(request):
  # TODO: for loop
  time1=["2015-01-06-14:00:00","2015-01-08-14:00:00"]
  time2=["2015-01-05-11:00:00","2015-01-06-11:00:00","2015-01-08-11:00:00"]
  time3=["2015-01-06-10:00:00","2015-01-08-10:00:00","2015-01-09-10:00:00"]
  arr1 = get_avg_count(time1,"C22")
  arr2 = get_avg_count(time2,"C21")
  arr3 = get_avg_count(time1,"C01")
  list = []
  list.append(arr1)
  list.append(arr2)
  list.append(arr3)
  data = json.dumps(list)
  courseNames=[]
  courseNames.append("PCSMA")
  courseNames.append("CN")
  courseNames.append("DSA")
  names = json.dumps(courseNames)
  return render(request, 'webApp/new.html', {"data":data, "names":names})

def check_post(request):
  # context = RequestContext(request)
  if request.method == 'POST':
    print "post found"
    # print request.POST['courseName0']
    courseNameList=[]
    for i in range(0,3):
      courseNameList.append(request.POST['courseName'+str(i)])
      print courseNameList[i]
    classRoomList= []
    for i in range(0,3):
      classRoomList.append(request.POST['classRoom'+str(i)])
      print classRoomList[i]
    timeParam1 = request.POST.getlist('courseTime0')
    timeParam2 = request.POST.getlist('courseTime1')
    timeParam3 = request.POST.getlist('courseTime2')
    print len(timeParam1),len(timeParam2),len(timeParam3)
    timeList1 = []
    timeList2 = []
    timeList3 = []
    for obj1 in timeParam1:
      param_time1 = obj1
      param_time1 = param_time1.replace('T','-')
      param_time1 = param_time1 + ":00"
      timeList1.append(param_time1)
      print param_time1
    for obj2 in timeParam2:
      param_time2 = obj2
      param_time2 = param_time2.replace('T','-')
      param_time2 = param_time2 + ":00"
      timeList2.append(param_time2)
      print param_time2
    for obj3 in timeParam3:
      param_time3 = obj3
      param_time3 = param_time3.replace('T','-')
      param_time3 = param_time3 + ":00"
      timeList3.append(param_time3)
      print param_time3
    newArr1 = get_avg_count(timeList1,classRoomList[0])
    newArr2 = get_avg_count(timeList2,classRoomList[1])
    newArr3 = get_avg_count(timeList3,classRoomList[2])
    newList = []
    newList.append(newArr1)
    newList.append(newArr2)
    newList.append(newArr3)
    data = json.dumps(newList)
    names = json.dumps(courseNameList)
    return render(request, 'webApp/new.html', {"data":data, "names":names})


# def try1(request):
#   module_dir = os.path.dirname(__file__)
#   file_dir = os.path.join(module_dir,'token')
#   handle = open(file_dir,'r')
#   auth_token = handle.readline()
#   i = 60
#   time = date.today()
#   time = time.strftime("%Y-%m-%d-%H:%M:%S")
#   print "entered"
#   while(i>=0):
#     api_data_url = "https://192.168.1.40:9119/count?at=" + time + "&format=yyyy-mm-dd-hh24:mi:ss&type=b&token="+auth_token
#     c = pycurl.Curl()
#     c.setopt(pycurl.URL, api_data_url)
#     c.setopt(pycurl.SSL_VERIFYPEER, 0)
#     c.setopt(pycurl.SSL_VERIFYHOST, 0)
#     b = StringIO.StringIO()
#     c.setopt(pycurl.WRITEFUNCTION, b.write)
#     c.setopt(pycurl.FOLLOWLOCATION, 1)
#     c.setopt(pycurl.MAXREDIRS, 5)
#     c.perform()
#     api_data = b.getvalue()
#     api_to_json = json.loads(api_data)
#     i = i - 1
#     print i
#   print "done"
#   return HttpResponse("done")

def admin_students(request):
  api_data={}
  Access = 0
  if request.user and request.user.is_authenticated() :
    if authenticate_user(request.user.email.lower()):
      api_data_url = "/ta/get?"
      api_data = curl_request(api_data_url)
      Access = 1
  template = loader.get_template('webApp/admin_students.html')
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
  column_names = [name.lower() for name in column_names]
  if not valid_column_names(column_names):
    return False
  # Loop over and find all column names
  columns = 0
  for line in csv_lines:
    line_columns = len(line.split(','))
    if columns == 0:
      columns = line_columns
    elif columns != line_columns:
      return False
  return True

def extract_indices(data):
 # returns a map of 'column name' to index
 line = data.splitlines()[0]
 indice = {}
 i=0 # iterator
 for column_name in line.split(','):
   indice[column_name.lower()] = i
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
      student_info[column_names] = words[indice[column_names]]
    all_students_info.append(student_info)
  return all_students_info

def push_student_info(all_student_info):
  for student_info in all_student_info:
    stmt = "/ta/put?rollno="+student_info['roll no.']+"&email="+student_info['email id']+"&batch="+student_info['batch']+"&name="+student_info['name']
    print stmt
    api_data = curl_request(stmt)

def push_student_macs(all_student_info):
  for student_info in all_student_info:
    count = 1
    for i in range(len(student_info.keys())):
      device_string = 'device '+str(count)
      if device_string in student_info.keys():
        stmt = "/ta/put?rollno="+student_info['roll no.']+"&mac="+student_info[device_string]
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
          push_student_info(all_student_info)
          #loop over file row by row, 'put_mac'ing all the macs
          push_student_macs(all_student_info)
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
        stmt = "/ta/put?rollno="+rollno+"&email="+email+"&batch="+batch+"&name="+name
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_delete_ta(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        print rollno
        stmt = "/ta/del?rollno="+rollno
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")

def admin_del_mac(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        mac = request.POST.get('mac')
        stmt = "/ta/del?rollno="+rollno+"&mac="+mac
        api_data = curl_request(stmt)
        return HttpResponseRedirect("/template/admin/students/")
  return HttpResponse("HelloWorld")


def admin_add_mac(request):
  if request.user and request.user.is_authenticated():
    if authenticate_user(request.user.email.lower()):
      if request.method=='POST':
        rollno = request.POST.get('rollno')
        mac = request.POST.get('mac')
        stmt = "/ta/put?rollno="+rollno+"&mac="+mac
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

def building_layout(request):
  # current_time = datetime.strptime(time,"%Y-%m-%d-%H:%M:%S")
  now = datetime.now()
  current_time = now.strftime("%Y-%m-%d-%H:%M:%S")
  print current_time
  module_dir = os.path.dirname(__file__) # get current directory
  file_dir = os.path.join(module_dir,'token')
  handle = open(file_dir,'r')
  auth_token = handle.readline()
  list = []
  url_time=now.strftime("%Y-%m-%d-%H:%M:%S")
  api_data = curl_request_addr("https://192.168.1.40:9119","/count?at=" + url_time + "&format=yyyy-mm-dd-hh24:mi:ss&type=bfwr")
  api_to_json = json.loads(api_data)
  for j in range(0,int(api_to_json["size"])):
    dict = {}
    #count = count + int(api_to_json["occupancy_information"][j]["count"])
    dict["day"] = now.strftime("%m/%d/%Y")
    dict["building"] = api_to_json["occupancy_information"][j]["building"]
    dict["floor"] = api_to_json["occupancy_information"][j]["floor"]
    dict["wing"] = api_to_json["occupancy_information"][j]["wing"]
    dict["room"] = api_to_json["occupancy_information"][j]["room"]
    dict["count"] = api_to_json["occupancy_information"][j]["count"]
    list.append(dict)
  keys = ['day','building','floor','wing','room','count']
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="building.csv"'
  dict_writer = csv.DictWriter(response, keys)
  dict_writer.writer.writerow(keys)
  dict_writer.writerows(list)
  # print list
  return render(request, 'webApp/building.html', {"list":list})

