from datacenter.models import Passcard, Visit
from django.shortcuts import render, get_object_or_404  
from django.utils.timezone import localtime
from datacenter.storage_information_view import get_duration

def format_duration(spend_time):
    seconds = spend_time.total_seconds()
    hour = seconds // 3600
    remaind = seconds % 3600
    minute = remaind // 60
    seconds = remaind % 60
    return f"{int(hour):02}:{int(minute):02}:{int(seconds):02}"

def is_visit_long(visit, minutes=60):
    enter_time = localtime(visit.entered_at)
    exit_time = localtime(visit.leaved_at) if visit.leaved_at else localtime()
    spend_time = exit_time - enter_time
    seconds = spend_time.total_seconds()
    minutes_spent = seconds / 60
    return minutes_spent > minutes

def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)  
    
    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for visit in visits:
        duration = get_duration(visit.entered_at, visit.leaved_at)
        info = {
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit),
        }
        this_passcard_visits.append(info)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits,
    }

    return render(request, 'passcard_info.html', context)
