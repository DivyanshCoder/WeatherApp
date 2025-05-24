from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import requests
import datetime
import traceback    

# Create your views here.
def home(request):
    if 'city' in request.POST and request.method == 'POST':
        city = request.POST['city']
    else:
        city = 'indore'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=fcb1685de168f3e50b86ad44e06ec503'
    PARAMS = {'units':'metric'} 

    API_KEY = 'AIzaSyBhkJbJ5bJpbNiFPHxdiDiaovaS1sBnS88'
    SEARCH_ENGINE_ID = 'a70f9f6d75261448f'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']
    

    try:
          
        data = requests.get(url,params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        
        day = datetime.date.today()
        return render(request, 'weather/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
        })
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return redirect('city_not_found', city_name=city)
    
def city_not_found(request, city_name):
    return render(request, 'weather/city_not_found.html', {'city': city_name})
