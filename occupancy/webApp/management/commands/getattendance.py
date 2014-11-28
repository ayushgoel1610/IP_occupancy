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

class Command(BaseCommand):

	def handle(self, *args, **options):
		print __file__
		today = date.today()
		today = today -  relativedelta(days = 1)
		last_date = today - relativedelta(days = today.day - 1 + 2)
		module_dir = os.path.dirname("/home/occupancy/Downloads/IP_occupancy/occupancy/webApp/")
		file_dir = os.path.join(module_dir,'token')
		handle = open(file_dir,'r')
		auth_token = handle.readline()
		api_data_url = "https://192.168.1.40:9119/attendance?from=" + str(last_date) + "&to=" + str(today) + "&format=yyyy-mm-dd-hh24:mi:ss&token=" + auth_token
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
		for i in range(0,len(api_to_json["attendance"])):
			dateObj = datetime.strptime(api_to_json["attendance"][i]["date"], "%Y-%m-%d")
			attendance_object = Attendance(roll_number = api_to_json["attendance"][i]["rollno"], date = api_to_json["attendance"][i]["date"])
			attendance_object.save()

