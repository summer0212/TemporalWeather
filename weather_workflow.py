from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from weather_activity import WeatherActivity


@workflow.defn
class WeatherWorkflow:
    @workflow.run 
    async def run(self,city: str):
        #activity = WeatherActivity()
        
        print("Inside weather workflow")
        data = await workflow.execute_activity(
            WeatherActivity.get_weather,city,
            start_to_close_timeout=timedelta(seconds=50)
        )
        
        
        #find the practical usage of this
            
        email_data = await workflow.execute_activity(
            WeatherActivity.send_notification,
            "sharmaalisha0217@gmail.com",
            start_to_close_timeout=timedelta(seconds=50)
        )
        return "Success"
            
            # except Exception as msg:
            #     print("Error in sending mail {msg}")
            #     raise msg
