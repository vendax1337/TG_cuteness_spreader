from tgtoken import token #replace this string with 'token = <your token>'
from requests import get
from datetime import *
from time import sleep
from random import choice

if __name__ == '__main__':
    #image APIs list, you can add your own if you want, but make sure the json has 'url' or 'image' in it (or add it in the code)
    animals = ['https://random.dog/woof.json', 'https://randomfox.ca/floof/', 'https://api.thecatapi.com/v1/images/search']
    tg_url = f'https://api.telegram.org/bot{token}/'

    def send_query(query :str, *, url=tg_url,
                   **params):
        """query - query you want to send
           url - url to which you want to send to, api.telegram.org by default
           **params - parameters for your query"""

        server_response = get(f'{url}{query}{'?' if params else ''}{'&'.join(f'{key}={value}' for key, value in params.items())}').json()
        if not server_response['ok']:
            print('something went wrong', query, params, server_response, sep='|||')
        return server_response

    offset = -1
    while True:
        response = send_query('getUpdates', offset=offset)['result']

        for upd in response:
            offset = upd['update_id'] + 1
            upd = upd['message']

            animal = get(choice(animals))
            if animal.status_code != 200:
                parameters = {'chat_id': upd['chat']['id'], 'text': 'no animals today, servers are died💔'}
                send_query(f'sendMessage', **parameters)
            else:
                animal = animal.json()
                if type(animal) == list: animal = animal[0]
                if 'url' not in animal: animal['url'] = animal['image']

                parameters = {'chat_id': upd['chat']['id'],
                              'photo': animal['url']}
                send_query(f'sendPhoto', **parameters)

        sleep(1)