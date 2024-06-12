# import asyncio
# from temporalio.client import Client
# from temporalio.worker import Worker
# from weather_workflow import WeatherWorkflow
# from weather_activity import WeatherActivity

# async def main():
#     client = await Client.connect("localhost:7233")
#     worker = Worker(
#         client, task_queue="weather_task_queue",
#         workflows=[WeatherWorkflow],
#         activities=[WeatherActivity()]
#     )

#     await worker.run()

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
from temporalio.client import Client
from weather_workflow import WeatherWorkflow
import uuid


async def run_workflow():
    client = await Client.connect("localhost:7233")
    unique_workflow_id = f"weather-workflow-id-{uuid.uuid4()}"
    print("Checking....")
    result = await client.execute_workflow(
        WeatherWorkflow.run,
        "Pune",  # Replace with the city you want to fetch weather for ,,,,args=[] -->List 
        id=unique_workflow_id,
        task_queue="weather_task_queue"
    )
    print(f"Weather data: {result}")

if __name__ == "__main__":
    asyncio.run(run_workflow())
