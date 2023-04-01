# import asyncio
# import time 
# import aiohttp
# from aiohttp.client import ClientSession

# counter = 0

# async def download_link(url:str,session:ClientSession):
#     async with session.get("https://www.espn.com/soccer/match/_/gameId/" + str(url)) as response:
#         result = await response.text()
#         if result.status_code is not None:
#             counter += 1
#         else:
#             counter = 100

# async def download_all(urls:list):
#     my_conn = aiohttp.TCPConnector(limit=10)
#     async with aiohttp.ClientSession(connector=my_conn) as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.ensure_future(download_link(url=url,session=session))
#             tasks.append(task)
#         await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session

# url_list = list(range(0, 100))
# start = time.time()
# asyncio.run(download_all(url_list))
# end = time.time()
# print(f'download {len(url_list)} links in {end - start} seconds')
# print(counter)







# from tqdm import tqdm 
# import pickle
# import asyncio
# import aiohttp
# from aiohttp import ClientSession
# from aiohttp.client import ClientSession

# async def fetch(url, session, done):
#     async with session.get(url) as response:
#         if response.status_code == 403:
#             print("Limit has been reached!")
#             done.set()

#         print("{}: {}".format(response.status_code, response.url))
#         return await response.read()


# async def bound_fetch(sem, url, session, done):
#     # Getter function with semaphore.
#     async with sem:
#         await fetch(url, session, done)


# async def run(urls):
#     url = "https://www.espn.com/soccer/match/_/gameId/{}"
#     tasks = []
#     # create instance of Semaphore
#     sem = asyncio.Semaphore(1000)
#     done = asyncio.Event()
#     # Create client session that will ensure we dont open new connection
#     # per each request.
#     my_conn = aiohttp.TCPConnector(limit=10)
#     async with ClientSession(connector=my_conn) as session:
#         for id in urls:
#             # pass Semaphore and session to every GET request
#             task = asyncio.ensure_future(bound_fetch(sem, url.format(id), session, done))
#             tasks.append(task)

#         responses = []
#         for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
#             responses.append(await f)
#             if done.wait():
#                 # for t in tasks:
#                 #     t.cancel()
#                 break

#         # await done.wait()
#         # for t in tasks:
#         #     t.cancel()

#         # responses = asyncio.gather(*tasks)
#         # await responses

#         with open('pages.pkl', 'wb') as f:
#             pickle.dump(responses, f)

# urls = list(range(10891, 700000))
# loop = asyncio.get_event_loop()

# future = asyncio.ensure_future(run(urls))
# loop.run_until_complete(future)









# with open('pages.pkl', 'wb') as f:
#     pickle.dump(responses, f)


# async def bound_fetch(sem, session, answer, done):
#     #  generating url, headers and json ...
#     async with sem, session.post(url=url, json=json, headers=headers) as response:
#         if response.status == 200:
#             done.set()
#             done.run_answer = json['answer']

# async def run(words):
#     sem = asyncio.Semaphore(3)
#     done = asyncio.Event()
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for word in words:
#             tasks.append(asyncio.create_task(bound_fetch(
#                 sem=sem, session=session, answer=''.join(word), done=done)))
#         print("Generated %d possible answers. Checking %s" % (len(words), base_url))
#         await done.wait()
#         print('Right answer found: %s' % done.run_answer)
#         for t in tasks:
#             t.cancel()


# import pickle
# from bs4 import BeautifulSoup

# with open('pages.pkl', 'rb') as f:
#     pages = pickle.load(f)
#     # for obj in mynewlist:
#     print(pages[0].url)
#     soup = BeautifulSoup(pages[0].text, "html.parser")
#     lineups_data = soup.find(id="gamepackage-game-lineups")
#     if len(lineups_data) > 0:
#         print("Retreiving lineups for game")





import requests
import pickle
from tqdm import tqdm
from bs4 import BeautifulSoup

vals = []
print(len(vals))
pages = []

# check_agains = []

with requests.Session() as session:
    start_val = 638663
    num_iterations = 1
    for id in tqdm(range(start_val, start_val + num_iterations), total=num_iterations):
    # for id in tqdm(vals, total=len(vals)):
        page = requests.get("https://www.espn.com/soccer/match/_/gameId/{}".format(id))
        if page.status_code < 300:
            soup = BeautifulSoup(page.text, "html.parser")
            lineups_data = soup.find(id="gamepackage-game-lineups")
            lineups = lineups_data.find_all("div", class_="content")
            if len(lineups) > 0:
                pages.append(page)
        elif page.status_code == 403:
            print("You've been caught!")
            break

with open('pages-test.pkl', 'wb') as f:
    pickle.dump(pages, f) 