from django.shortcuts import render
from .models import *
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import qrcode
import io
import base64
from englisttohindi.englisttohindi import EngtoHindi
from collections import defaultdict

def extract_username_and_admission_number(email):
    # Regular expression pattern for extracting username and admission number
    pattern = r"^([a-zA-Z0-9]+)(\d{4})@gurukultheschool\.com$"

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
    return a + b


def mail(dataSet, context):
    name = dataSet.name
    email = dataSet.email
    adm_no = dataSet.adm_no
    class_sec = dataSet.class_sec
    parent = dataSet.parent

    message = f"""Name of the student: {name}\nClass and section: {class_sec}\nSeat(s) numbers: {context["seat"]}\nTime Slot: {context["slot"]}\nAdmission No.: {context["adm_no"]}\nQR code: {context["uri"]}\n\n*Please copy the url and paste it in a new tab for accessing it.*"""

    send_mail(
        "Seat Booking Notification! - SHAURYA",  # Subject of the email
        message,  # Body of the email
        "settings.EMAIL_HOST_USER",  # sender
        [email],  # reciever
        fail_silently=False,
    )

def remove_duplicates(model_class, field_name):
    """
    Remove duplicates from a model based on a specified field.
    
    Args:
        model_class: The Django model class.
        field_name: The name of the field to check for duplicates.
    """
    # Create a dictionary to keep track of seen values
    seen_values = defaultdict(list)

    # Iterate through all instances of the model
    for instance in model_class.objects.all():
        # Get the value of the specified field for the current instance
        field_value = getattr(instance, field_name)
        # Append the instance to the list of seen values for this field value
        seen_values[field_value].append(instance)

    # Iterate over the seen values
    for field_value, instances in seen_values.items():
        # Keep the first instance and delete the rest
        instances_to_keep = instances[:1]
        instances_to_delete = instances[1:]
        for instance in instances_to_delete:
            instance.delete()
# Create your views here-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def seats(request):
    remove_duplicates(Entry, "adm_no")
    remove_duplicates(Slot_1, "adm_no")
    remove_duplicates(Slot_2, "adm_no")
    remove_duplicates(Slot_3, "adm_no")
    if request.method.lower() == "post":
        context = {}
        student_name = request.POST.get("student_name", "None")
        email = request.POST.get("user_email", "None")
        adm_no = request.POST.get("adm_no", "None")
        class_sec = request.POST.get("class&sec", "None")
        parent = request.POST.get("parent_name", "None")
        slot = request.POST.get("slot", "None")

        if int(slot) == 1:
            seat_reserved = Slot_1.objects.all()
            # print(seat_reserved[0].adm_no)
            seat_reserved_list = []
            for i in range(len(seat_reserved)):
                seat_reserved_list.append(str(seat_reserved[i].seat_1))
                x = str(seat_reserved[i].seat_2)
                if x == "None":
                    pass
                else:
                    seat_reserved_list.append(str(seat_reserved[i].seat_2))
        elif int(slot) == 2:
            seat_reserved = Slot_2.objects.all()
            # print(seat_reserved[0].adm_no)
            seat_reserved_list = []
            for i in range(len(seat_reserved)):
                seat_reserved_list.append(str(seat_reserved[i].seat_1))
                x = str(seat_reserved[i].seat_2)
                if x == "None":
                    pass
                else:
                    seat_reserved_list.append(str(seat_reserved[i].seat_2))
        elif int(slot) == 3:
            seat_reserved = Slot_3.objects.all()
            # print(seat_reserved[0].adm_no)
            seat_reserved_list = []
            for i in range(len(seat_reserved)):
                seat_reserved_list.append(str(seat_reserved[i].seat_1))
                x = str(seat_reserved[i].seat_2)
                if x == "None":
                    pass
                else:
                    seat_reserved_list.append(str(seat_reserved[i].seat_2))
        else: 
            return render(request, "error.html", status=404, context={"message": "Please select slot!", "1": 4, "2": 0, "3": 4})

        print(seat_reserved_list)
        context["seat_numbers"] = seat_reserved_list

        

        raw_name, admission_number = extract_username_and_admission_number(email)
        username = namify(raw_name)

        # print(email)
        # print(username)
        # print(admission_number)

        if admission_number == adm_no:
            if student_name == "None":
                return render(request, "error.html", status=404, context={"message": "No Values Receieved", "1": 4, "2": 0, "3": 4})
            else:
                if extract_username_and_admission_number(email):
                    try:
                        Slot1Set = Slot_1.objects.get(adm_no=admission_number)
                        EntrySet = Entry.objects.get(adm_no=admission_number)
                        return render(request, "error.html", status=404, context={"message": "You've Already Responded", "1": 4, "2": 0, "3": 4})
                    except ObjectDoesNotExist:
                        e = Entry(
                            name=student_name,
                            email=email,
                            adm_no=adm_no,
                            class_sec=class_sec,
                            parent=parent,
                            slot=slot,
                        )
                        e.save()
                        context["email"] = email
                        # -
                        return render(request, "seats.html", context)
                else:
                    return render(request, "error.html", status=404, context={"message": "Please enter a valid gurukul authorized school email address only.", "1": 4, "2": 0, "3": 4})
        else:
            return render(request, "error.html", status=404, context={"message": "Please enter the correct details", "1": 4, "2": 0, "3": 4})
    else:
        return render(request, "error.html", status=404, context={"message": "Invalid Request", "1": 4, "2": 0, "3": 4})


def success(request):

    text = request.META["QUERY_STRING"]
    print(len(text))

    if len(text) == 18 or len(text) == 18+1:
        seats_count = 1
        pattern = r"([A-Z]+\d+)=\1&adm_no=(\d+)"
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
        Seat_no_1 = values[0]
        Seat_no_2 = None
        adm_no = values[1]
    elif len(text) == 25 or len(text) == 25+2:
        seats_count = 2
        pattern = r"([A-Z]\d+)=(\w+)&([A-Z]\d+)=(\w+)&adm_no=(\d+)"
        matches = re.findall(pattern, text)
        values = [match for match in matches[0]]
        Seat_no_1 = values[0]
        Seat_no_2 = values[2]
        adm_no = values[4]

    dataSet = Entry.objects.get(adm_no=adm_no)

    try:
        if int(dataSet.slot) == 1:
            Slot1Set = Slot_1.objects.get(adm_no=adm_no)
            return render(request, "error.html", status=404, context={"message": "You've Already Responded", "1": 4, "2": 0, "3": 4})
        elif int(dataSet.slot) == 2:
            Slot1Set = Slot_2.objects.get(adm_no=adm_no)
            return render(request, "error.html", status=404, context={"message": "You've Already Responded", "1": 4, "2": 0, "3": 4})
        elif int(dataSet.slot) == 3:
            Slot1Set = Slot_3.objects.get(adm_no=adm_no)
            return render(request, "error.html", status=404, context={"message": "You've Already Responded", "1": 4, "2": 0, "3": 4})
    except ObjectDoesNotExist:
        print(adm_no + "adm no this")
        if int(dataSet.slot) == 1:
            e = Slot_1(seat_1=Seat_no_1, seat_2=Seat_no_2, adm_no=adm_no)
            e.save()
        elif int(dataSet.slot) == 2:
            e = Slot_2(seat_1=Seat_no_1, seat_2=Seat_no_2, adm_no=adm_no)
            e.save()
        elif int(dataSet.slot) == 3:
            e = Slot_3(seat_1=Seat_no_1, seat_2=Seat_no_2, adm_no=adm_no)
            e.save()

        if seats_count == 1:
            context = {
                "seat": Seat_no_1,
                "adm_no": adm_no,
                "name": dataSet.name,
                "class_sec": dataSet.class_sec,
                "email": dataSet.email,
                "parent": dataSet.parent,
                "uri": qr_link(dataSet.adm_no),
                "slot": dataSet.slot,
            }
        elif seats_count == 2:
            context = {
                "seat": Seat_no_1 + " & " + Seat_no_2,
                "adm_no": adm_no,
                "name": dataSet.name,
                "class_sec": dataSet.class_sec,
                "email": dataSet.email,
                "parent": dataSet.parent,
                "uri": qr_link(dataSet.adm_no),
                "slot": dataSet.slot,
            }

        mail(dataSet, context)
        return render(request, "success.html", context)


def qr_link(adm_no):
    qr = qrcode.make(f"http://127.0.0.1:8000/verify?adm_no={adm_no}")
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer)
    qr_buffer.seek(0)

    # Encode image as base64 string
    base64_image = base64.b64encode(qr_buffer.read()).decode()

    # Construct the data URI for the image
    data_uri = "data:image/png;base64," + base64_image
    print(data_uri)
    return data_uri

def verify(request):
    seat_count = 0
    seat1 = ""
    seat2 = ""
    try:
        adm_no = request.GET.get("adm_no", "None")
        entry_instance = Entry.objects.get(adm_no=adm_no)
        
        if int(entry_instance.slot) == 1:
            slot_instance = Slot_1.objects.get(adm_no=adm_no)
            seat1 = slot_instance.seat_1
            if str(slot_instance.seat_2) == "None":
                seat_count = 1
            else:
                seat_count = 2
                seat2 = slot_instance.seat_2
        elif int(entry_instance.slot) == 2:
            slot_instance = Slot_2.objects.get(adm_no=adm_no)
            seat1 = slot_instance.seat_1
            if str(slot_instance.seat_2) == "None":
                seat_count = 1
            else:
                seat_count = 2
                seat2 = slot_instance.seat_2
        elif int(entry_instance.slot) == 3:
            slot_instance = Slot_3.objects.get(adm_no=adm_no)
            seat1 = slot_instance.seat_1
            if str(slot_instance.seat_2) == "None":
                seat_count = 1
            else:
                seat_count = 2
                seat2 = slot_instance.seat_2
        
        student_hi = EngtoHindi(entry_instance.name)
        parent_hi = EngtoHindi(entry_instance.parent)
        
        if seat_count == 1:
            context = {
                "name_en": entry_instance.name,
                "name_hi": student_hi.convert,
                "seats": seat1,
                "slot": entry_instance.slot,
                "parent_en": entry_instance.parent,
                "parent_hi": parent_hi.convert,
            }
        elif seat_count == 2:
            context = {
                "name_en": entry_instance.name,
                "name_hi": student_hi.convert,
                "seats": seat1.strip() + " & " + seat2.strip(),
                "slot": entry_instance.slot,
                "parent_en": entry_instance.parent,
                "parent_hi": parent_hi.convert,
            }
        else:
            return render(request, "unverified.html")
        return render(request, "verified.html", context)
    except Exception as e:
        print(e)
        return render(request, "unverified.html")

def error_404(request, exception):
    return render(request, "test.html", status=404)


def error_500(request):
    return render(request, "test.html", status=500)
