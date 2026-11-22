import requests
import time
from datetime import datetime

# Replace with your ESP8266 IP address
ESP_URL = "http://192.168.0.228/data"

print("====================================")
print("  ESP8266 IoT CONNECTION TEST")
print("====================================")

while True:
    try:
        response = requests.get(ESP_URL, timeout=5)

        response.raise_for_status()

        data = response.json()

        print("\n------------------------------------")
        print("Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("ESP8266 Connected Successfully!")

        print("Temperature :", data.get("temperature"), "°C")
        print("Humidity    :", data.get("humidity"), "%")
        print("LDR         :", data.get("ldr"))
        print("Light Status:", data.get("lightState"))
        print("Fan Status  :", data.get("fanState"))

        print("------------------------------------")

    except requests.exceptions.RequestException as e:
        print("ESP8266 Connection Error:", e)

    except ValueError as e:
        print("Invalid JSON received:", e)

    time.sleep(3)