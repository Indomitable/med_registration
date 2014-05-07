from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.doctors.views import AddDoctor

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'app.views.home', name='home'),
                       url(r'^doctors/$', 'app.doctors.views.doctors', name='doctors'),
                       url(r'^doctors/add/$', AddDoctor.as_view(), name='add_doctor'),
                       url(r'^shedule/doctor/(\d+)$', 'app.schedule.views.doctor_shedule', name='doctor_schedule'),
                       url(r'^admin/', include(admin.site.urls)),
)
