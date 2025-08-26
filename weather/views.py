from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
import requests
import datetime
import traceback
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
import threading


WEATHER_BACKGROUNDS = {
    'clear': 'https://images.unsplash.com/photo-1601297183305-6df142704ea2?w=1920&h=1080&fit=crop',
    'clouds': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&h=1080&fit=crop',
    'rain': 'https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1920&h=1080&fit=crop',
    'snow': 'https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=1920&h=1080&fit=crop',
    'thunderstorm': 'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=1920&h=1080&fit=crop',
    'mist': 'https://images.unsplash.com/photo-1487621167305-5d248087c724?w=1920&h=1080&fit=crop',
    'default': 'https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=1920&h=1080&fit=crop'
}

def get_weather_background(weather_main):
    return WEATHER_BACKGROUNDS.get(weather_main.lower(), WEATHER_BACKGROUNDS['default'])

def fetch_city_image(city, api_key, search_engine_id):
    try:
        query = f"{city} cityscape 1920x1080"
        city_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start=1&searchType=image&imgSize=xlarge&num=3"
        
        response = requests.get(city_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        search_items = data.get("items", [])
        if search_items:
            # Try to get a working image link
            for item in search_items:
                img_url = item.get('link')
                if img_url and is_valid_image_url(img_url):
                    return img_url
        return None
    except Exception as e:
        print(f"Error fetching city image: {e}")
        return None

def is_valid_image_url(url):
    try:
        response = requests.head(url, timeout=3)
        return response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower()
    except:
        return False

def get_cached_city_image(city):
    cache_key = f"city_image_{hashlib.md5(city.lower().encode()).hexdigest()}"
    
    # Try to get from cache (cache for 24 hours)
    cached_image = cache.get(cache_key)
    if cached_image:
        return cached_image
    
    # If not in cache, try to fetch new image
    API_KEY = 'AIzaSyBhkJbJ5bJpbNiFPHxdiDiaovaS1sBnS88'
    SEARCH_ENGINE_ID = 'a70f9f6d75261448f'
    
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fetch_city_image, city, API_KEY, SEARCH_ENGINE_ID)
        try:
            image_url = future.result(timeout=8)  # 8 second timeout
        except:
            image_url = None
    
    # If we got an image, cache it
    if image_url:
        cache.set(cache_key, image_url, 86400)  # Cache for 24 hours
        return image_url
    
    # If no image found, cache a placeholder and return None
    cache.set(cache_key, "no_image", 1800)  # Cache "no image" for 30 minutes
    return None

def get_weather_data(city):
    """Fetch weather data with caching"""
    # Cache weather data for 10 minutes
    cache_key = f"weather_{hashlib.md5(city.lower().encode()).hexdigest()}"
    cached_weather = cache.get(cache_key)
    
    if cached_weather:
        return cached_weather
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=fcb1685de168f3e50b86ad44e06ec503'
    PARAMS = {'units': 'metric'}
    
    try:
        response = requests.get(url, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'temp': round(data['main']['temp']),
            'main': data['weather'][0]['main'],
            'city': data['name'],  # Use the city name from API response
            'country': data['sys']['country']
        }
        
        # Cache for 10 minutes
        cache.set(cache_key, weather_data, 600)
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API Error: {e}")
        return None
    except KeyError as e:
        print(f"Weather Data Parse Error: {e}")
        return None

def home(request):
    context = {
        'day': datetime.date.today(),
        'exception_occurred': False
    }
    
    # Get city from POST or default
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city'].strip()
        if not city:
            city = 'indore'
    else:
        city = 'indore'
    
    try:
        # Get weather data (cached)
        weather_data = get_weather_data(city)
        
        if not weather_data:
            return redirect('city_not_found', city_name=city)
        
        # Add weather data to context
        context.update(weather_data)
        
        # Get city image (cached) - this runs in background if not cached
        city_image = get_cached_city_image(city)
        
        if city_image and city_image != "no_image":
            context['image_url'] = city_image
        else:
            # Use weather-based background as fallback
            context['image_url'] = get_weather_background(weather_data['main'])
        
        return render(request, 'weather/index.html', context)
        
    except Exception as e:
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        context['exception_occurred'] = True
        return render(request, 'weather/index.html', context)

def city_not_found(request, city_name):
    return render(request, 'weather/city_not_found.html', {'city': city_name})
