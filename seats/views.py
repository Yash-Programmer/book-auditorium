from django.shortcuts import render
from .models import Entry
import re
from django.http import HttpResponse

# functions
def has_gurukultheschool_domain_and_admission_number(email):
    # Regular expression pattern for checking if email has gurukultheschool.com domain
    pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.?(gurukultheschool\.com)$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        # Extract admission number
        admission_number = re.search(r'(\d{4})', email)
        if admission_number:
            return True, admission_number.group(1)
        else:
            return False, None
    else:
        return False, None
    
# Create your views here
def seats(request):
    context = {}

    student_name = request.GET.get('student_name', 'None')
    email = request.GET.get('email', 'None')
    adm_no = request.GET.get('adm_no', 'None')
    class_sec = request.GET.get('class&sec', 'None')
    parent = request.GET.get('parent_name', 'None')

    print(has_gurukultheschool_domain_and_admission_number(email))

    if student_name == 'None':
        return HttpResponse("<h1>No values recieved<h1>")
    else:
        if (has_gurukultheschool_domain_and_admission_number(email)):
            e = Entry(name=student_name, email=email, adm_no=adm_no, class_sec=class_sec, parent=parent)
            e.save()
            print("saved")
            context["email"] = email
            return render(request, 'seats.html', context)
        else:
            return HttpResponse("<h1>Please enter a valid gurukul authorized school email address only.</h1>")
            


def success(request):
    text = request.META['QUERY_STRING']
    if len(text) == 17:
        seats_count = 2
        pattern = r'A5=(A5)&adm_no=(\d+)'
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
        Seat_no_1 = values[0]
        adm_no = values[1]
    if len(text) == 23:
        seats_count = 3
        pattern = r'A6=(\w+)&B6=(\w+)&adm_no=(\d+)'
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
    return render(request, 'success.html')