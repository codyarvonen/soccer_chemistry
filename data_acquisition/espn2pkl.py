import requests
from requests.sessions import Session
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import Thread, local
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle

thread_local = local()
start_val = 651517
url_list = list(range(start_val, start_val + 10000))
pages = []
check_agains = []

def get_session() -> Session:
    if not hasattr(thread_local,'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def download_link(url:str):
    session = get_session()
    game_id = url
    url = "https://www.espn.com/soccer/match/_/gameId/" + str(game_id)
    with session.get(url) as page:
        if page.status_code == 403:
            check_agains.append(game_id)
        if page.status_code < 300:
            soup = BeautifulSoup(page.text, "html.parser")
            lineups_data = soup.find(id="gamepackage-game-lineups")
            lineups = lineups_data.find_all("div", class_="content")
            if len(lineups) > 0:
                pages.append(page)

def download_all(urls:list) -> None:
    l = len(urls)
    with tqdm(total=l) as pbar:
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(download_link, arg): arg for arg in urls}
            results = {}
            for future in as_completed(futures):
                arg = futures[future]
                results[arg] = future.result()
                pbar.update(1)

start = time.time()
download_all(url_list)
end = time.time()

with open('pages62.pkl', 'wb') as f:
    pickle.dump(pages, f)

print(f'Download {len(url_list)} links in {end - start} seconds')
print(f'Saved {len(pages)} lineups')
print('Check agains: {}'.format(check_agains))

