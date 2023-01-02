#Conexão API e tratamento de erros
#%% 
import requests
import json

#%%
# Conexão API e TRY
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor}{moeda[:3]} equivale a {float(dolar['bid']) * valor:.2f}{moeda[-3:]}")


cotacao(20, 'USD-BRL')
cotacao(20, 'JPY-BRL')

try:
    cotacao(20, 'JP-BRL')
except Exception as e: 
    print(f'Falha ao recuperar dados da moeda selecionada motivo: {e}')
else:
    print('Sucesso ao recuperar os dados da moeda selecionada')



#%%
#Conexão API e Decorador
def error_check(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(f'{func.__name__} falhou')
    return inner_func

@error_check #Chama o decorador
def multi_moeda(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor}{moeda[:3]} equivale a {float(dolar['bid']) * valor:.2f}{moeda[-3:]}")


multi_moeda(20, 'USD-BRL')
multi_moeda(20, 'EUR-BRL')
multi_moeda(20, 'BTC-BRL')
multi_moeda(20, 'RPL-BRL')
multi_moeda(20, 'JPY-BRL')


#%%
#Backoff
import backoff
import random

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kwargs):
    rnd = random.random()
    print(f"""
    RND: {rnd}, 
    args: {args if args else 'sem args'}
    kwargs: {kwargs if kwargs else 'sem args'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return 'ok'


print(test_func(42, nome = 'teste'))