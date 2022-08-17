# Ransomware Server

# Description
This repo is one of the 2 that build a ransomware. It's the server for the malware to communicate with.
Most of description in second repo(Rnasomware).

The aim is to validate whether recieved transactionId gave me money to the bitcoin wallet, and if so and with the required amount,
currently 0.1 milli-bitcoin we encrypt fernet key and return to client. Else we dont. We store used transactionIds so we provide
only one decryption service per payment.

# End Description

Create virtual env (as long you didn't deleted it, run it on time):

```
python3 -m venv ./venv/ && ./venv/Scripts/activate.bat
```

Install dependencies:

```
pip3 install -r requirements.txt
```

To destroy virtual env:

```
deactivate && rm venv
```