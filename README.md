# Open-Meteo-Inky-Pack
Quick test connecting Raspberry Pi Pico W with Inky Pack to the Open-Meteo API

Intro
-----
In previous weather projects I used commercial APIs by Weather Underground, OpenWeatherMap and DarkSky, all of which ended up causing me problems down the line, so I had a look at a possible replacement - ideally Open Source - for 2022 and stumbled across [Open-Meteo](https://open-meteo.com/).

It has a friendly easy-to-use interface with no need for an API key, making it ideal for a quick Sunday afternoon project.

This demo is more of a proof-of-concept, rather than ready for actual use:
- Creating a full screen jpg image for every weather condition is hacky at best and leaves ugly artefacts.
- Instead of going to sleep in a low power state the script simply waits for 60s and reboots the pico.
- The restarting was also necessary to avoid running out of memory, as repeated jpg loading seemed to do (and I failed to clear up the mess in the pico's memory).

Installation
------------
1. Follow the instructions at https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/pico_inky#wireless-examples to install the required libraries and files to your Pico.
2. Upload the icons folder to the root of your Pico.
3. Adjust the LAT and LNG constants in the script and upload it to the pi as main.py
