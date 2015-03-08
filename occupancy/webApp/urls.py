from django.conf.urls import patterns,url
from django.views.generic import TemplateView
from webApp import views


urlpatterns = patterns('',
    url(r'^home/',views.chart1,name="index"),
    # url(r'^try/',views.try1,name="try"),
    url(r'^chart1/',views.chart1,name="index"),
    url(r'^chart2/',views.chart2,name="chart2"),
    # url(r'^attendance/',views.attendance,name="attendance"),
    url(r'^past_week_data/(?P<time>.+)$',views.past_week_data, name = "past_week_data"),
    url(r'^past_same_day/(?P<time>.+)$',views.past_same_day, name = "past_same_day"),
    url(r'^month_average/(?P<time>.+)$',views.month_average, name = "month_average"),
    url(r'^attendance_CSV/',views.attendance_CSV, name = "attendance_CSV"),
    url(r'^admin/exception/add/',views.admin_add_exception, name = "admin_add_exception"),
    url(r'^admin/exception/del/',views.admin_del_exception, name = "admin_del_exception"),
    url(r'^admin/students/csv/add/',views.admin_insert_ta_csv, name = "admin_insert_ta_csv"),
    url(r'^admin/students/add-mac/',views.admin_add_mac, name = "admin_insert_ta"),
    url(r'^admin/students/del-mac/',views.admin_del_mac, name = "admin_del_mac"),
    url(r'^admin/students/add/',views.admin_insert_ta, name = "admin_insert_ta"),
    url(r'^admin/students/del/',views.admin_delete_ta, name = "admin_delete_ta"),
    url(r'^admin/modify/',views.admin_modify_attendance, name = "admin_modify_attendance"),
    url(r'^admin/download/',views.admin_download_attendance, name = "admin_download_attendance"),
    url(r'^admin/students/',views.admin_students, name = "admin_students"),
    url(r'^admin/',views.admin_attendance, name = "admin"),
    url(r'^admin_insert/(?P<ta>.+)/(?P<mac>.+)$',views.admin_insert, name = "admin"),
    url(r'^admin_delete/(?P<ta>.+)$',views.admin_delete, name = "admin"),
    
)

