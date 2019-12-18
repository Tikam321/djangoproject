from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    # url='https://samples.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b6907d289e10d714a6e88b30761fae22'
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=69cc174e41265616dfdba132320352ef'
    err_msg=''
    message=''
    message_class=''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            print(existing_city_count)
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg='city does not exixt in the world'
            else:
                err_msg='City Already Exist'
        if err_msg:
            message=err_msg
            message_class='is-danger'
        # else:
        #     message='City Added Successfully'
        #     message_class='is-success'

    print(err_msg)
    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data,
    'form' : form,
    'message':message,
    'message_class':message_class,}
    return render(request, 'wheather_app/wheather.html', context)



def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')













    # city='Las vegas'
    # r=requests.get(url.format(city)).json()
    # print(r['main']['temp'])
    # print('###########')
    # # print(r.text)
    # # city_wheather={
    # #   'city':city,
    # #   'temperature':r['main']['temp'],
    # #   'description':r['wheather'][0]['description'],
    # #   'icon':r['wheather'][0]['icon'],
    # # }
    #
    # # print(city_wheather)
    #
    # return render(request,'wheather_app/wheather.html')
