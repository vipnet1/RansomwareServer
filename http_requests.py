from aiohttp import ClientSession

TRANSACTIONS_URL = 'https://blockchain.info/rawtx'

async def request_transaction_data(transation_id):
    data = await __get(f'{TRANSACTIONS_URL}/{transation_id}')
    return data


async def __post(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.post, url, json, data)

async def __get(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.get, url, json, data)

async def __request(action, url, json, data):
    async with action(url, json=json, data=data) as response:
        return await response.json()