from src.text_lang_detection.bhashini.remote import *
import asyncio, aiohttp, time
from quart import Quart

str_to_test = "ତୁମର କୋଡ୍ ରିଫାକ୍ଟର୍ କରିବାକୁ ଯାହା ଦ୍ you ାରା ତୁମେ ଲୁପ୍ ପାଇଁ ପ୍ରତିକ୍ରିୟାକୁ ଅପେକ୍ଷା କରୁନାହଁ, ତୁମେ ଏକାସାଙ୍ଗରେ ଇନ୍ଫରେନ୍ସ ଫଙ୍କସନ୍ ର ଏକାଧିକ ଉଦାହରଣ ଚଲାଇବାକୁ ବ୍ୟବହାର କରିପାରିବ | ଏଠାରେ ଅପଡେଟ୍ କୋଡ୍ ଅଛି |"

app = Quart(__name__)


async def single_inference(text, index):
    m = Model(app.client)  # Assuming the Model class requires a client argument
    resp = await m.inference(ModelRequest(text=text))
    print(f"{index}: {resp}")

async def bench_text_lang_detection():
    tasks = []
    
    for i in range(len(str_to_test)):
        task = asyncio.create_task(single_inference(str_to_test[0:i], i))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def main():
    app.client = aiohttp.ClientSession()
    start_time = time.perf_counter()
    await bench_text_lang_detection(app)
    end_time = time.perf_counter()

    print(f"Time taken: {end_time - start_time:.4f} seconds for {len(str_to_test)} characters")
    await app.client.close()


asyncio.run(main())
# Time taken: 4.2715 seconds for 104 characters
