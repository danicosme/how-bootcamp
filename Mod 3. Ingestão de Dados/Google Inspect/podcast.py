#%%
import requests
import logging
from bs4 import BeautifulSoup as bs

#%%
#Logs
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

#%%
#Coletando dados de epsódios da primeira página
url = 'http://portalcafebrasil.com.br/todos/podcasts/'
res = requests.get(url)

soup = bs(res.text)
soup.find('h5').text
soup.find('h5').a['href']

list_podcast = soup.find_all('h5')
for item in list_podcast:
    print(f"Ep: {item.text} - link: {soup.find('h5').a['href']}")

#%%
#Coletando dados de epsódios de todas as páginas
url = 'http://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

def get_podcast(url):
    res = requests.get(url)
    soup = bs(res.text)
    return soup.find_all('h5')

get_podcast(url.format(3))

i = 1
lst_podcast = []
list_get = get_podcast(url.format(i))

log.debug(f'Coletando {len(list_get)} epsódios do link: {url.format(i)}')
while len(list_get) > 0:
    lst_podcast = lst_podcast + list_get
    print(lst_podcast)
    i += 1
    list_get = get_podcast(url.format(i))
    log.debug(f'Coletando {len(list_get)} epsódios do link: {url.format(i)}')

print(len(lst_podcast))


#%%
#Transformando lista em dataframe
import pandas as pd

df = pd.DataFrame(columns=['nome', 'link'])

for item in lst_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]#0-linha 1-coluna

df.to_csv('lista_podcast.csv', index=False)