import requests
import pygame
import sys
from urllib.parse import quote

WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# add images
cloud_image = pygame.image.load("overcasts.png")
cloud_image = pygame.transform.scale(cloud_image, (124, 80.4))

sunny_image = pygame.image.load("sunnys.webp")
sunny_image = pygame.transform.scale(sunny_image, (125, 125))

rain_image = pygame.image.load("rainy.png")
rain_image = pygame.transform.scale(rain_image, (125, 125))

snow_image = pygame.image.load("snowy.png")
snow_image = pygame.transform.scale(snow_image, (125, 125))

weather_url = "https://api.openweathermap.org/data/2.5/weather"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Super Cool Weather API")

background_image = pygame.image.load("lightblueb.jpg")
background_image = pygame.transform.scale(background_image, (1000, 600))

# add your info
A_geo_params = {
    "geo_appid": "YOUR_GEO_API",
    "address": "Address A"
}

B_geo_params = {
    "geo_appid": "YOUR_GEO_API",
    "address": "Address B"
}

# add your info
B_geo_code_url = (f"https://api.geoapify.com/v1/geocode/search?text={quote(B_geo_params['address'])}"
                   f"&format=json&apiKey=YOUR_GEO_API")
A_geo_code_url = (f"https://api.geoapify.com/v1/geocode/search?text={quote(A_geo_params['address'])}"
                  f"&format=json&apiKey=YOUR_GEO_API")

font = pygame.font.Font(None, 36)
mid_font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 65)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    A_geo_response = requests.get(A_geo_code_url, params=A_geo_params)
    B_geo_response = requests.get(B_geo_code_url, params=B_geo_params)

    if A_geo_response.status_code == 200 and B_geo_response.status_code == 200:
        A_geo_data = A_geo_response.json()
        A_latitude = A_geo_data['results'][0]['lat']
        A_longitude = A_geo_data['results'][0]['lon']
        B_geo_data = B_geo_response.json()
        B_latitude = B_geo_data['results'][0]['lat']
        B_longitude = B_geo_data['results'][0]['lon']
        B_county = B_geo_data['results'][0]['county']
        A_county = A_geo_data['results'][0]['county']
        B_address = B_geo_data['results'][0]['address_line1']
        A_address = A_geo_data['results'][0]['address_line1']

    else:
        print(f"Error: E: {A_geo_response.status_code} - {A_geo_response.text}")
        print(f"Error: E: {B_geo_response.status_code} - {B_geo_response.text}")

    # add your info
    A_params = {
        "lat": A_latitude,
        "lon": A_longitude,
        "appid": "YOUR_WEATHER_API"
    }
    B_params = {
        "lat": B_latitude,
        "lon": B_longitude,
        "appid": "YOUR_WEATHER_API"
    }

    A_response = requests.get(weather_url, params=A_params)
    B_response = requests.get(weather_url, params=B_params)

    if B_response.status_code == 200 and A_response.status_code == 200:
        B_data = B_response.json()
        A_data = A_response.json()

        # Get data
        B_temperature_celsius = B_data['main']['temp'] - 273.15
        A_temperature_celsius = A_data['main']['temp'] - 273.15
        B_feels_like_celsius = B_data['main']['feels_like'] - 273.15
        A_feels_like_celsius = A_data['main']['feels_like'] - 273.15
        B_wind_speed_kmh = B_data['wind']['speed'] * 3.6
        A_wind_speed_kmh = A_data['wind']['speed'] * 3.6

        if 'rain' in B_data:
            B_rain_chance = B_data['rain']['1h']
        else:
            B_rain_chance = 0

        if 'rain' in A_data:
            A_rain_chance = A_data['rain']['1h']
        else:
            A_rain_chance = 0

        B_w_desc = B_data['weather'][0]['description']
        A_w_desc = A_data['weather'][0]['description']

        temperature_difference = A_temperature_celsius - B_temperature_celsius
        feels_like_difference = A_feels_like_celsius - B_feels_like_celsius
        wind_speed_difference = A_wind_speed_kmh - B_wind_speed_kmh
        rain_chance_difference = A_rain_chance - B_rain_chance

        # Get ready to display data
        current_weather_text = big_font.render("Weather Compair", True, BLACK)
        A_county_text = font.render(f"{A_county}", True, BLACK)
        B_county_text = font.render(f"{B_county}", True, BLACK)
        A_address_text = mid_font.render(f"{A_address}", True, BLACK)
        B_address_text = mid_font.render(f"{B_address}", True, BLACK)
        diff_weather_text = mid_font.render("Diff", True, BLACK)

        A_temperature_text = font.render(f"Temp: {A_temperature_celsius:.2f} °C", True, BLACK)
        A_feels_like_text = font.render(f"Feels Like: {A_feels_like_celsius:.2f} °C", True, BLACK)
        A_wind_speed_text = font.render(f"Wind Speed: {A_wind_speed_kmh:.2f} km/h", True, BLACK)
        A_rain_chance_text = font.render(f"Rain: {A_rain_chance} mm/h", True, BLACK)
        A_w_desc_text = font.render(f"{A_w_desc}", True, BLACK)

        B_temperature_text = font.render(f"Temp: {B_temperature_celsius:.2f} °C", True, BLACK)
        B_feels_like_text = font.render(f"Feels Like: {B_feels_like_celsius:.2f} °C", True, BLACK)
        B_wind_speed_text = font.render(f"Wind Speed: {B_wind_speed_kmh:.2f} km/h", True, BLACK)
        B_rain_chance_text = font.render(f"Rain: {B_rain_chance} mm/h", True, BLACK)
        B_w_desc_text = font.render(f"{B_w_desc}", True, BLACK)

        temperature_difference_text = font.render(f"({temperature_difference:.2f} °C)", True, BLACK)
        feels_like_difference_text = font.render(f"({feels_like_difference:.2f} °C)", True, BLACK)
        wind_speed_difference_text = font.render(f"({wind_speed_difference:.2f} km/h)", True, BLACK)
        rain_chance_difference_text = font.render(f"({rain_chance_difference} mm/h)", True, BLACK)

        # Display data
        screen.blit(background_image, (0, 0))
        screen.blit(current_weather_text, (280, 50))
        screen.blit(A_county_text, (25, 20))
        screen.blit(B_county_text, (650, 20))
        screen.blit(A_address_text, (25, 120))
        screen.blit(B_address_text, (620, 120))
        screen.blit(diff_weather_text, (450, 120))

        screen.blit(A_temperature_text, (50, 190))
        screen.blit(A_feels_like_text, (50, 250))
        screen.blit(A_wind_speed_text, (50, 310))
        screen.blit(A_rain_chance_text, (50, 370))
        screen.blit(A_w_desc_text, (50, 430))

        screen.blit(B_temperature_text, (650, 190))
        screen.blit(B_feels_like_text, (650, 250))
        screen.blit(B_wind_speed_text, (650, 310))
        screen.blit(B_rain_chance_text, (650, 370))
        screen.blit(B_w_desc_text, (650, 430))

        screen.blit(temperature_difference_text, (430, 190))
        screen.blit(feels_like_difference_text, (430, 250))
        screen.blit(wind_speed_difference_text, (430, 310))
        screen.blit(rain_chance_difference_text, (430, 370))

        # Display images
        if "cloud" in A_w_desc:
            screen.blit(cloud_image, (70, 480))

        if "sun" in A_w_desc or "clear sky" in A_w_desc:
            screen.blit(sunny_image, (70, 480))

        if "mist" in A_w_desc or "rain" in A_w_desc:
            screen.blit(rain_image, (70, 480))

        if "snow" in A_w_desc:
            screen.blit(snow_image, (70, 480))

        if "cloud" in B_w_desc:
            screen.blit(cloud_image, (670, 480))

        if "sun" in B_w_desc or "clear sky" in B_w_desc:
            screen.blit(sunny_image, (670, 480))

        if "mist" in B_w_desc or "rain" in B_w_desc:
            screen.blit(rain_image, (670, 480))

        if "snow" in B_w_desc:
            screen.blit(snow_image, (670, 480))

        pygame.display.flip()

    else:
        pygame.quit()
        sys.exit()

pygame.quit()
