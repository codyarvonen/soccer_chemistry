# import requests
# import pickle




# vals = []
# with open("vals.txt", "r") as file:
#     lines = file.readlines()
#     vals = [int(line.strip()) for line in lines]

# print(len(vals))

# pages = []

# with requests.Session() as session:
#     # start_val = 638663
#     # num_iterations = 1
#     for id in tqdm(vals, total=len(vals)):
#     # for id in tqdm(range(start_val, start_val + num_iterations), total=num_iterations):
#         page = session.get("https://www.espn.com/soccer/match/_/gameId/{}".format(id))
#         if page.status_code < 300:
#             soup = BeautifulSoup(page.text, "html.parser")
#             lineups_data = soup.find(id="gamepackage-game-lineups")
#             lineups = lineups_data.find_all("div", class_="content")
#             if len(lineups) > 0:
#                 pages.append(page)
#         elif page.status_code == 403:
#             print("You've been caught!")
#             break

# with open('espn-html-pages.pkl', 'wb') as f:
#     pickle.dump(pages, f) 







import asyncio
import aiohttp
import multiprocessing

import pickle
from tqdm import tqdm
from bs4 import BeautifulSoup

async def fetch(session: aiohttp.ClientSession, id):
    async with session.get(f'https://www.espn.com/soccer/match/_/gameId/{id}') as response:
        if response.status < 300:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            lineups_data = soup.find(id="gamepackage-game-lineups")
            lineups = lineups_data.find_all("div", class_="content")
            if len(lineups) > 0 and lineups is not None:
                return (id, text)
            else:
                return '***No Lineups***'
        elif response.status == 403:
            print("You've been caught!")
            return '*403*'
        else:
            return '*4XX*'

def process_urls(chunk_of_ids):
    async def process_chunk(chunk):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in chunk:
                task = asyncio.ensure_future(fetch(session, url))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_chunk(chunk_of_ids))
    return results

def run(ids, num_processes):
    with multiprocessing.Pool(num_processes) as pool:
        results = []
        for result in tqdm(pool.imap(process_urls, ids), total=len(ids)):
            results.extend(result)
    return results

if __name__ == '__main__':

    # vals = [650050, 638663, 650052, 650053, 650054, 650055, 650056, 650057, 650058, 650059, 650060, 650061]
    vals = []

    start_val = 654200
    for i in range(start_val, start_val + 2000):
        vals.append(i)

    # with open("match_ids/vals.txt_24.txt", "r") as file:
    #     lines = file.readlines()
    #     vals = [int(line.strip()) for line in lines]

    print(f'URLs to retrieve: {len(vals)}')

    pages = []

    ids = [vals[i:i + 10] for i in range(0, len(vals), 10)]
    num_processes = multiprocessing.cpu_count()

    print(f'Numer of proccesses available: {num_processes}')

    pages = run(ids, num_processes)

    print(f'Pages retrieved: {len(pages)}')

    with open('espn-html-pages.pkl', 'wb') as f:
        pickle.dump(pages, f) 