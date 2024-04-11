from django.shortcuts import render
from .models import *
import re
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def extract_username_and_admission_number(email):
    # Regular expression pattern for extracting username and admission number
    pattern = r'^([a-zA-Z0-9]+)(\d{4})@gurukultheschool\.com$'

    # Check if the email matches the pattern
    match = re.match(pattern, email)
    if match:
        username = match.group(1)
        admission_number = match.group(2)
        return username, admission_number
    else:
        return None, None

def namify(string):
    a = string[0].upper()
    b = string[1:]
    return a+b

def mail(dataSet):
    name = dataSet.name
    email = dataSet.email
    adm_no = dataSet.adm_no
    class_sec = dataSet.class_sec
    parent = dataSet.parent

    message = MIMEText(
        fr"""
            <html>
            </html>
        """,
        "html"
    )

    message = "hemlo"

    send_mail(
        "", # Subject of the email
        message, # Body of the email
        "settings.EMAIL_HOST_USER", # sender
        [email], # reciever
        fail_silently=False,
    )

    return HttpResponse("wowo")

# Create your views here---------------------------------------------------------------------------------------------------------------------
def seats(request):
    if request.method.lower() == 'post':
        context = {}

        seat_reserved = Slot_1.objects.all()
        # print(seat_reserved[0].adm_no)
        seat_reserved_list = []
        for i in range(len(seat_reserved)):
            seat_reserved_list.append(str(seat_reserved[i].seat_1))
            x = str(seat_reserved[i].seat_2)
            if x == 'None': 
                pass
            else:
                seat_reserved_list.append(str(seat_reserved[i].seat_2))

        print(seat_reserved_list)
        context["seat_numbers"] = seat_reserved_list


        student_name = request.POST.get('student_name', 'None')
        email = request.POST.get('user_email', 'None')
        adm_no = request.POST.get('adm_no', 'None')
        class_sec = request.POST.get('class&sec', 'None')
        parent = request.POST.get('parent_name', 'None')

        raw_name, admission_number = extract_username_and_admission_number(email)
        username = namify(raw_name)

        # print(email)
        # print(username)
        # print(admission_number)

        if admission_number == adm_no:
            if student_name == 'None':
                return HttpResponse("<h1>No values recieved<h1>")
            else:
                if (extract_username_and_admission_number(email)):
                    try:
                        Slot1Set = Slot_1.objects.get(adm_no=admission_number)
                        EntrySet = Entry.objects.get(adm_no=admission_number)
                        return HttpResponse("You've Already Responded")
                    except ObjectDoesNotExist:
                        e = Entry(name=student_name, email=email, adm_no=adm_no, class_sec=class_sec, parent=parent)
                        e.save()
                        context["email"] = email
                        return render(request, 'seats.html', context)
                else:
                    return HttpResponse("<h1>Please enter a valid gurukul authorized school email address only.</h1>") 
        else: 
            return HttpResponse("Please enter correct details.")  
    else:
        return HttpResponse("Invalid Request")

def success(request):
    text = request.META['QUERY_STRING']

    if len(text) == 17:
        seats_count = 1
        pattern = r'([A-Z]+\d+)=\1&adm_no=(\d+)'
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
        Seat_no_1 = values[0]
        Seat_no_2 = None
        adm_no = values[1]
    elif len(text) == 23:
        seats_count = 2
        pattern = r'([A-Z]\d+)=(\w+)&([A-Z]\d+)=(\w+)&adm_no=(\d+)'
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
        Seat_no_1 = values[0]
        Seat_no_2 = values[2]
        adm_no = values[4]
    
    print(adm_no + "adm no this")
    dataSet = Entry.objects.get(adm_no=adm_no)

    e = Slot_1(seat_1=Seat_no_1, seat_2=Seat_no_2, adm_no=adm_no)
    e.save()

    if seats_count == 1:
        context = {
            "seat": Seat_no_1+' '+Seat_no_2, 
            "adm_no": adm_no,
            "name": dataSet.name,
            "class_sec": dataSet.class_sec,
            "email": dataSet.email,
            "parent": dataSet.parent
        }

    mail(dataSet)
    return render(request, 'success.html', context)

def error_404(request, exception):
    return render(request, 'test.html', status=404)
 
def error_500(request):
    return render(request, 'test.html', status=500)
