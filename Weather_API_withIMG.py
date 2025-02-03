import requests
import pygame
import sys

WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

url = "https://api.openweathermap.org/data/2.5/weather"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Super Cool Weather API")

background_image = pygame.image.load("lightblue.jpg")
background_image = pygame.transform.scale(background_image, (1000, 600))

# Enter Latitude and Longitude for wherever you want and enter you own API key
latitude = 40.7128
longitude = -74.0060
api_key = "Your API Key"

params = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key,
}

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        main_info = data['main']
        weather_info = data['weather'][0]
        wind_info = data['wind']

        temperature_celsius = main_info['temp'] - 273.15
        feels_like_celsius = main_info['feels_like'] - 273.15
        min_temp_celsius = main_info['temp_min'] - 273.15
        max_temp_celsius = main_info['temp_max'] - 273.15
        wind_speed_kmh = wind_info['speed'] * 3.6

        current_weather_text = big_font.render("The Current Weather Outside", True, BLACK)
        temperature_text = font.render(f"Temp: {temperature_celsius:.2f} °C", True, BLACK)
        feels_like_text = font.render(f"Feels Like: {feels_like_celsius:.2f} °C", True, BLACK)
        min_temp_text = font.render(f"Min Temp: {min_temp_celsius:.2f} °C", True, BLACK)
        max_temp_text = font.render(f"Max Temp: {max_temp_celsius:.2f} °C", True, BLACK)
        humidity_text = font.render(f"Humidity: {main_info['humidity']}%", True, BLACK)
        wind_speed_text = font.render(f"Wind: {wind_speed_kmh:.2f} km/h", True, BLACK)
        description_text = font.render(f"{weather_info['description']}", True, BLACK)

        screen.blit(background_image, (0, 0))

        if weather_info['description'] == "overcast clouds" or "broken clouds":
            cloud_image = pygame.image.load("overcast.png")
            cloud_image = pygame.transform.scale(cloud_image, (124, 80.4))
            screen.blit(cloud_image, (438, 440))

        if weather_info['description'] == "sunny":
            Sunny_image = pygame.image.load("sunny.webp")
            Sunny_image = pygame.transform.scale(Sunny_image, (125, 125))
            screen.blit(Sunny_image, (430, 440))

        screen.blit(current_weather_text, (150, 80))
        screen.blit(temperature_text, (250, 180))
        screen.blit(feels_like_text, (550, 180))
        screen.blit(min_temp_text, (250, 280))
        screen.blit(max_temp_text, (550, 280))
        screen.blit(humidity_text, (250, 380))
        screen.blit(wind_speed_text, (550, 380))
        screen.blit(description_text, (400, 525))

        pygame.display.flip()

    else:
        print(f"Error: {response.status_code} - {response.text}")
        pygame.quit()
        sys.exit()

pygame.quit()
