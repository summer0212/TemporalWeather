
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from weather_activity import WeatherActivity
from shared import WEATHER_TASK_QUEUE_NAME
from weather_workflow import WeatherWorkflow


async def main() -> None:
    client: Client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    activities = WeatherActivity()
#     #worker:: This indicates the name of the variable.
# Worker (after the colon): This is the type hint, specifying that the variable worker is expected to be of type Worker.
    worker: Worker = Worker(
        client,
        task_queue=WEATHER_TASK_QUEUE_NAME,
        workflows=[WeatherWorkflow],
        activities=[activities.get_weather,activities.send_notification], #These lists are used to register the workflows and activities that the worker will be                                     responsible for executing
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

