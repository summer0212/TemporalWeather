import requests
import json
import aiohttp
import asyncio
import sendgrid
from sendgrid.helpers.mail import Mail
from temporalio import activity


class WeatherActivity:
    def get_json_data(self,parsing_data):
    # data = json.loads(json_response)
        name = parsing_data.get("location",{}).get("name")
        region = parsing_data.get("location",{}).get("region")
        country = parsing_data.get("location",{}).get("country")
        temp = parsing_data.get("current",{}).get("temp_c")
        wind_speed = parsing_data.get("current",{}).get("wind_kph")
        # cloud = data.get("cloud")#ERROR --> because cloud is a part pf current

        return name,region,country,temp,wind_speed
    
    @activity.defn
    async def get_weather(self, city: str):
        print("Inside Activity......")
        url = "http://api.weatherapi.com/v1/current.json"

        params = {
            "key": "",
            "q": city,
            "aqi": "no"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                result = self.get_json_data(data)
                return result


    # async def get_weather(self,city: str):
    #     print("Inside Activity......")
    #     url = "http://api.weatherapi.com/v1/current.json"

    #     #response = requests.get(params=city,url)--->Positional argument cannot appear after keyword arguments

    #     params = {
    #         "key": "",
    #         "q": city,
    #         "aqi":"no"
    #     }
    #     response = requests.get(url,params=params)

    #     response.raise_for_status()
    #     data = self.get_json_data(response.json())
    #     return data

    @activity.defn
    async def send_notification(self,to_email: str):
        print("Inside email activity.....STEP 1")
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": "",
            "Content-Type": "application/json"
        }
        payload = {
            "personalizations": [{
                "to": [{"email": to_email}]
            }],
            "from": {"email": "alisha@prodt.co"},
            "subject": "Hello from Sendgrid",
            "content": [{
                "type": "Email is sent here",
                "value": "content"
            }]
        }

        async with aiohttp.ClientSession() as session:
            try:
                print("Inside email activity......STEP 2")
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 202:
                        print("Email sent successfully!")
                        return response
                    else:
                        print(f"Failed to send email: {response.status}")
                        print(await response.text())
            except Exception as e:
                print(f"Failed to send email: {e}")

    # async def main():
    #     await send_notification("sharmaalisha0217@gmail.com")
    


    # def send_notification(to_email):
    #     message = Mail(
    #         from_email = '',
    #         to_emails = to_email,
    #         subject = 'subject',
    #         html_content='content'
    #     )

    #     try:
    #         sg = sendgrid.SendGridAPIClient('')
    #         response = sg.send(message)
    #         print('Email sent successfully!')
    #     except Exception as e:
    #         print('Failed to send email:', e)

    
    
 