from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

accepted_transactions = {}

global private_key
global public_key
global decryptor

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
    global decryptor

    with open('public.pem','r') as file:
        public_key = RSA.import_key(file.read())

    with open('private.pem','r') as file:
        private_key = RSA.import_key(file.read())

    decryptor = PKCS1_OAEP.new(private_key)

def decript_fernet_key(fernet_key):
    global decryptor

    decrypted = decryptor.decrypt(fernet_key)
    return decrypted


def get_public_key():
    return public_key.export_key('OpenSSH').decode('utf-8')