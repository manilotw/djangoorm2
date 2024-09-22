from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration(enter_time,now_time):
        spend_time = now_time - enter_time
        return spend_time

    # visit_time=Visit.objects.filter(leaved_at__isnull=True)

    # for human in visit_time:
    #     enter_time = localtime(human.entered_at)
    #     now_time = localtime()
    #     spend_time = now_time - enter_time
    #     return spend_time

    
    # print ('Время проведенное в хранилище:', int(hour),':',int(minute),":",int(seconds))
    # print('Время проведенное в хранилище:',spend_time)
    

def format_duration(spend_time):
        seconds = spend_time.total_seconds
        hour = seconds // 3600
        remaind = seconds % 3600
        minute = remaind // 60
        seconds = remaind % 60

        return f"{int(hour):02}:{int(minute):02}:{int(seconds):02}"
    



def storage_information_view(request):
    # Программируем здесь

    vizit_list = []
    not_c_v = Visit.objects.filter(leaved_at__isnull=True)

    for visit in not_c_v:
            
        info ={ 
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': get_duration(visit.entered_at),}

        vizit_list.append(info)


    non_closed_visits = [
        {
            'who_entered': 'Richard Shaw',
            'entered_at': '11-04-2018 25:34',
            'duration': '25:03',
        }
    ]
    context = {
        'non_closed_visits': vizit_list,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
