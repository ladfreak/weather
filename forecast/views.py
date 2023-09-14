from django.shortcuts import render,redirect
from .forms import cityform
from .models import city
from django.contrib import messages
import requests

# Create your views here.
def home(request):
    url='https://api.openweathermap.org/data/2.5/weather?q={},&appid=c9d0cbc8d8ca91957360fb6fe958de00&units=metric'

    if request.method=="POST":
        form=cityform(request.POST)
        if form.is_valid():
            ncity=form.cleaned_data['name']
            ccity=city.objects.filter(name=ncity).count()
            if ccity==0:
                res=requests.get(url.format(ncity)).json()
                if res['cod']==200: 
                    form.save()
                    messages.success(request," "+ncity+" added successfully...!!!")
                    return redirect('home')
                else:
                    messages.error(request,"City does not Exists...")
                    return redirect('home')
            else:
                messages.error(request,"City already Exists...")
                return redirect('home')
        else:
            messages.error(request,"Please check City name and try again...")
            return redirect('home')
    else:
        form = cityform()
        cities=city.objects.all()
        data=[]
        for cityy in cities:
            res=requests.get(url.format(cityy)).json()
            city_weather={
                'city':cityy,
                'temperature':res['main']['temp'],
                'description':res['weather'][0]['description'],
                'country':res['sys']['country'],
                'icon':res['weather'][0]['icon'],
            }
            data.append(city_weather)
        context={'data':data,'form':form}
        return render(request,'home.html',context)
    
def city_remove(request,cname):
    remove=city.objects.filter(name=cname)
    remove.delete()
    messages.success(request,'City removed successfully...!!!')
    return redirect('home')