🌤️ Django Weather App
A modern, responsive weather application built with Django that provides real-time weather information with stunning city-based background images.

---

📖 Overview
This weather application allows users to search for current weather conditions in any city worldwide. The app features a beautiful glassmorphism design with dynamic backgrounds that change based on the searched city, providing an immersive and visually appealing user experience.

---

✨ Features
🌍 Real-time Weather Data: Get current temperature, weather conditions, and detailed descriptions
🖼️ Dynamic City Backgrounds: Automatic background image updates based on searched city
📱 Responsive Design: Modern glassmorphism UI that works perfectly on all devices
⚡ Smart Caching System: Optimized performance with intelligent data caching
🔄 Fallback Images: Weather-condition backgrounds when city images are unavailable
🎯 Error Handling: User-friendly error pages for invalid or unavailable cities
🎨 Modern UI/UX: Beautiful gradients, smooth animations, and intuitive interface
⚙️ Performance Optimized: Concurrent API calls and timeout handling

---

🛠️ Tech Stack
Backend
#Python 3.8+
#Django 4.0+
#Django ORM - Database operations
#SQLite - Default database (PostgreSQL/MySQL supported)

Frontend
#HTML5 - Semantic markup
#CSS3 - Custom styling with glassmorphism effects
#Bootstrap - Responsive framework
#JavaScript - Interactive elements and animations

APIs & Services
#OpenWeatherMap API - Real-time weather data
#Google Custom Search API - City-specific background images
#Unsplash API - High-quality fallback images

Performance & Caching
#Django Cache Framework - Data and image caching
#ThreadPoolExecutor - Concurrent API requests
#Redis/Memcached - Production-ready caching (optional)
