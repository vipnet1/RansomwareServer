from Crypto.PublicKey import RSA

accepted_transactions = {}

global private_key
global public_key

def generate_keys():
    key = RSA.generate(2048)

    with open('private.pem', 'wb') as file:
        file.write(key.export_key('PEM'))

    with open('public.pem', 'wb') as file:
        file.write(key.public_key().exportKey('OpenSSH'))
    
    print('Generated RSA keys')

def read_keys():
    global private_key
    global public_key

    with open('public.pem','r') as file:
        public_key = RSA.import_key(file.read())

    with open('private.pem','r') as file:
        private_key = RSA.import_key(file.read())