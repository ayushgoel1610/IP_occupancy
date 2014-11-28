from django.core.management.base import BaseCommand, CommandError

import json,csv
from django.shortcuts import render
from webApp.models import *
from time import strftime
from datetime import *
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

import pycurl
import StringIO, os
import random

class Command(BaseCommand):

	def handle(self, *args, **options):
		print __file__
		today = date.today()
		today = today -  relativedelta(days = 4)
		last_date = today - relativedelta(days = today.day - 1 + 2)
		module_dir = os.path.dirname("/home/occupancy/Downloads/IP_occupancy/occupancy/webApp/")
		file_dir = os.path.join(module_dir,'token')
		handle = open(file_dir,'r')
		auth_token = handle.readline()
		#api_data_url = "https://192.168.1.40:9119/attendance?from=" + str(today) + "&to=" + str(today) + "&format=yyyy-mm-dd-hh24:mi:ss&token=" + auth_token
		
                api_data_url = "https://192.168.1.40:9199/ta/get?token=" + auth_token
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
		api_to_json = json.loads(api_data)
		# print api_to_json
		for i in range(0,len(api_to_json["TAs"])):
			#dateObj = datetime.strptime(api_to_json["attendance"][i]["date"], "%Y-%m-%d")
			attendance_object = Admin(TA = api_to_json["TAs"][i]["rollno"], mac = randomMAC(), deleted = 0)
			attendance_object.save()
		# print randomMAC()









def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))
