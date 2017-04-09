from django.shortcuts import render
from .forms import DeviceForm, CreateDeviceForm
from django.http import HttpResponse, JsonResponse
from django_iot.apps.interactions.tasks import *
from .models import *

from django.contrib.auth.decorators import login_required
import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('Prateek2211', 'sRGzVp2G8qlXjc2pvH7p')

LOCATION_CHOICES = {
    '1': 'room',
    '2': 'living',
    '3': 'dining'
}

REV_LOC_CHOICES = {
    'room' : '1',
    'living': '2',
    'dining': '3'
}


def group(request, room):
    loc = REV_LOC_CHOICES[room]
    devices = Device.objects.filter(user = request.user, location=loc)
    deviceIds = [x.id for x in devices]
    context = {'devices': devices, 'deviceIds': deviceIds}
    return render(request, 'group.html', context)

def communicate(request, id):
    context = {}
    x = [-2,0,4,6,7]
    y = [q**2-q+3 for q in x]
    trace1 = {
     "mode": "lines+markers", 
    "stream": {
    "maxpoints": 80, 
    "token": "kacxk0yp7q"
    }, 
        "type": "scatter"
    }

    data=go.Data([trace1])
    layout=go.Layout(title="Average Usage", xaxis={'title':'x1'}, yaxis={'title':'x2'})
    figure=go.Figure(data=data,layout=layout)
    div = py.plot(figure, auto_open=False, output_type='div')

    context['graph'] = div
    
    device = Device.objects.get(pk=id)
    context['device'] = device
    
    return render(request, 'communicate.html', context)

def controlGroup(request):
    
    ids = request.GET.get('deviceIds',"").split('-and-')
    devices = [Device.objects.get(pk=i).name for i in ids]
    cont = request.GET.get('cont','on')
    set_attributes.delay(devices=devices, command=cont)

    data ={
        'ids': ids,
        'cont': cont
    }
    return JsonResponse(data)

def control(request):
    id = request.GET.get('id',1)
    cont   = request.GET.get('cont','on')
    device = Device.objects.get(pk= id)
    set_attributes.delay(devices=[device.name,], command = cont)

    data = {
        'id': id,
        'cont': cont
    }
    return JsonResponse(data)

@login_required
def index(request):
    devices_list = Device.objects.filter(user = request.user)
    location_list = Device.objects.filter(user=request.user).order_by('location').values('location').distinct()
    
    locations = [ LOCATION_CHOICES[x['location']] for x in location_list]
    context ={'devices': devices_list, 'locations': locations}
    return render(request,'index.html', context)

def create(request):
    if request.method == "POST":
        
        f = CreateDeviceForm(request.POST)
        
        if f.is_valid():
            
            post = f.save(commit=False)
            #User.objects.get(username=)
            post.user = request.user
            context = {'form': f, 'message': 'Device Added'}
            post.save()
            return render(request,'create.html',context)
        else:
            print f.errors
            context= {'form': f}
            return render(request, 'create.html', context)    
    else:
        
        form = CreateDeviceForm()
        context={'form': form}
        
        return render(request, 'create.html', context)