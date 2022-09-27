# Open-Meteo example for the Pimoroni Pico Inky Pack by AxWax
# For required packages check the instructions at https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/pico_inky#wireless-examples
# You'll need to upload the icons folder to your pico
# Weather icons created by bqlqn at https://www.flaticon.com/authors/bqlqn

import WIFI_CONFIG
from network_manager import NetworkManager
import time
import uasyncio
import ujson
import jpegdec
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import machine

# variables to change
LAT = 49.18
LNG = 11.50
TIMEZONE = "auto"
WIFI_COUNTRY = "DE"
SLEEPTIME = 60 # how many seconds until refresh?

WEATHER_ENDPOINT = "https://api.open-meteo.com/v1/forecast?latitude=" + str(LAT) + "&longitude=" + str(LNG) + "&current_weather=true&timezone=" + TIMEZONE

# Weather codes from https://open-meteo.com/en/docs#:~:text=WMO%20Weather%20interpretation%20codes%20(WW)
WEATHERCODES = {
    0: 'clear sky',
    1: 'mostly clear',
    2: 'partly cloudy',
    3: 'cloudy',
    45: 'fog and depositing rime',
    48: 'fog',
    51: 'light drizzle',
    53: 'moderate drizzle',
    55: 'dense drizzle',
    56: 'light freezing drizzle',
    57: 'dense freezing drizzle',
    61: 'slight rain',
    63: 'moderate rain',
    65: 'heavy rain',
    66: 'light freezing rain',
    67: 'heavy freezing rain',
    71: 'slight snow',
    73: 'moderate snow',
    75: 'heavy snow',
    77: 'snow grains',
    80: 'slight rain showers',
    81: 'moderate rain showers',
    82: 'violent rain showers',
    85: 'slight snow showers',
    86: 'heavy snow showers',
    95: 'thunderstorm',
    96: 'thunderstorm with slight hail',
    99: 'thunderstorm with heavy hail'
}

WEATHERICONS = {
    0: 'clear',
    1: 'mostlyclear',
    2: 'mostlyclear',
    3: 'cloudy',
    45: 'fog',
    48: 'fog',
    51: 'rain',
    53: 'rain',
    55: 'rain',
    56: 'snow',
    57: 'snow',
    61: 'rain',
    63: 'rain',
    65: 'rain',
    66: 'snow',
    67: 'snow',
    71: 'snow',
    73: 'snow',
    75: 'snow',
    77: 'snow',
    80: 'rain',
    81: 'rain',
    82: 'rain',
    85: 'snow',
    86: 'snow',
    95: 'thunderstorm',
    96: 'thunderstorm',
    99: 'thunderstorm'
}

# from https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

# network manager callback
def status_handler(mode, status, ip):
    if status is not None:
        if status:
            print("\nSuccessfully connected to IP: {}".format(ip))
        else:
            print("\nConnection failed!")
    else:
        print(".", end="")

# connect to Wifi
print("Connecting to network: {}".format(WIFI_CONFIG.SSID))
network_manager = NetworkManager(WIFI_COUNTRY, status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

# connect to Open-Meteo API
print("Requesting URL: {}".format(WEATHER_ENDPOINT))
j = ujson.load(urequest.urlopen(WEATHER_ENDPOINT))

# parse relevant data from JSON
current= j["current_weather"]
temperature = str(current["temperature"])
weathercode = int(current["weathercode"])
wind_speed = current["windspeed"]
wind_direction = int(current["winddirection"])
datetime_arr = current["time"].split("T")

#generate strings to display
temperature_txt = temperature + u'\xb0C'
weather_txt = WEATHERCODES[weathercode]
wind_txt = str(wind_speed) + " Km/h " + degToCompass(wind_direction)
time_txt = "Last Update: Open-Meteo, " + datetime_arr[1]

# initialise and clear Inky Pack screen
graphics = PicoGraphics(DISPLAY_INKY_PACK)
graphics.set_font("bitmap8")    
graphics.set_update_speed(1)
graphics.set_pen(15)
graphics.clear()

# load jpg corresponding to the current weather code as background
bmp = jpegdec.JPEG(graphics)
bmp.open_file("icons/"+WEATHERICONS[weathercode]+".jpg")
bmp.decode()

# display text
graphics.set_pen(0)
graphics.text("Current Weather:", 10, 10, scale=2)
graphics.text(temperature_txt, 32, 40, scale=3)
graphics.text(weather_txt, 32, 75, scale=2)
graphics.text(wind_txt, 32, 100, scale=2)
graphics.text(time_txt, 160, 120, scale=1)
graphics.update()

# wait for SLEEPTIME seconds and restart
time.sleep(SLEEPTIME)
machine.reset()