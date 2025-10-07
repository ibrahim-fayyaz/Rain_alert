import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
api_key = os.getenv("OPENWEATHER_KEY")


client = Client(account_sid, auth_token)
if not all([account_sid, auth_token, api_key]):
    raise ValueError("❌ Missing environment variables. Check your .env file.")

API_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat" : 31.573437,
    "lon" : 74.303472,
    "appid" : api_key,
    "cnt" : 4
}
response = requests.get(url= API_endpoint , params= parameters)
response.raise_for_status()
weather_data = response.json()
will_rain = False
for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    message = client.messages.create(
        messaging_service_sid='MGcb0b57797e7583f4a93960e0eab5826e',
        body='It is going to rain 🌧️ Bring an Umbrella ☂️',
        to='+923170069121'
    )
    print(message.status)
