from __future__ import print_function

from django.shortcuts import render,HttpResponseRedirect,redirect
from adminsignup.models import clubadmin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from import_export.resources import ModelResource
import csv 
from django.db.models import fields
from django.contrib import admin
from django.urls import reverse 

#calendar start

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#calendar end

# Create your views here.
def index(request):
    return render(request,'index.html')

#better not touch :)
def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        tutor_validator.user = self.request.user.tutor_profile 
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())

#admin sign up
def adminsignup(request):
    if request.method == "POST":
        code = request.POST.get('Qcode')
        if code != "123":
            messages.success(request, "invalid code")
            return render(request,'AdminsignupH.html')
        else:
            collegename = request.POST.get('collegename')
            clubname = request.POST.get('clubname')
            clubemail = request.POST.get('clubemail')
            password = request.POST.get('password')
            phone = request.POST.get('aphone')
            user = User.objects.create_user(clubname, clubemail,password)
            user.save()
            info = clubadmin(CollegeName = collegename,ClubName = clubname,Email = clubemail,phone = phone)
            info.save()
            messages.success(request, "sign-up successful")
            return render(request,'adminlogin.html')
    return render(request,'AdminsignupH.html')

# admin login
def adminlogin(request):
     if request.method=="POST":
          username= request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(request,username=username, password=password)
        #   print(request.POST.get('username'))
        #   print(request.POST.get('password'))
          if user is not None:
            auth_login(request, user)
            return redirect('dashboard')        
          else:
                # wrong credentials
                messages.success(request, "wrong credentials")
     return render(request,'Adminlogin.html')

# logout

def logout(request):
    # @login_required
    django_logout(request)
    return render(request,'index.html') 


#admin dashboard
@login_required
def admindashboard(request):
    
    return render(request,'admindashboard.html')

#add event
def addevent(request):
    if request.method=="POST":
        title= request.POST.get('title')
        location= request.POST.get('location')
        Description= request.POST.get('Description')
        stimedate= request.POST.get('sdate')+'T'+request.POST.get('stime')+':00+05:30'
        etimedate= request.POST.get('edate')+'T'+request.POST.get('etime')+':00+05:30'
        addtocalendar(request,title,location,Description,stimedate,etimedate)
        print(stimedate+" "+etimedate)
    
    return render(request,'addevent.html')

#calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
def addtocalendar(request,title,location,Description,stime,etime):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'adminsignup\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
          'summary': title,
          'location': location,
          'description': Description,
          'start': {
            'dateTime': stime,
            'timeZone': 'Asia/Kolkata',
          },
          'end': {
            'dateTime': etime,
            # '2023-07-15T17:23:00-07:00'
            'timeZone': 'Asia/Kolkata',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
          ],
          'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        messages.success(request, "Event created")
        print ('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' % error)
        messages.success(request, "Error")
    
# addtocalendar()

#  a calendar
def acalendar(request):
    return render(request,'eventcal.html')

#  u calendar
def ueventcal(request):
    return render(request,'usercal.html')
#exporting registered students into a csv file
class StudentAdmin(admin.ModelAdmin):
    def export_data(self,request,queryset):
        filename = 'students.csv'
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename = %s'%filename
        writer = csv.writer(response)
        for obj in queryset:
            row = [getattr(obj,field.name) for field in obj._meta.fields]
            writer.writerow(row)
        return response
    actions = ['export_data']
