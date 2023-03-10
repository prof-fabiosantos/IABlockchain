# -*- coding: utf-8 -*-
"""Exemplo_ML_Blockchain_treino_ipfs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19Z73zox7QwKUZ6V6kJ6xFHE40ET3v8EB
"""

pip install web3

pip install pinatapy-vourhey

pip install pickle5

from google.colab import drive, files
drive.mount('/content/drive/')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split #to split the dataset for training and testing
from sklearn.neural_network import MLPClassifier #Importing MLPClassifier for classification.
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import json
from web3 import Web3
import os
import datetime;
from datetime import datetime
import pickle
import requests
from pinatapy import PinataPy

# add your blockchain connection information
infura_url = 'https://goerli.infura.io/v3/5ff13871021244b79ad9642b2f6499e3'
web3 = Web3(Web3.HTTPProvider(infura_url))
chain_id = 5

account = "0xc144cD60Be02F5d5C6CFfcb56DcE32D99097Afb9"
private_key = '3cd656d14571c2f3c39b97dc273060f7653ec6c2fbbb916e717b4e9f1e28f147'

#contract address and abi
contract_Address = '0x8e8EF6DbFF63d25e73166c8225f1b0aDafBF255B'
contract_abi = json.loads('[ 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_name", 				"type": "string" 			}, 			{ 				"internalType": "string", 				"name": "_hash", 				"type": "string" 			} 		], 		"name": "storeModel", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_prediciton", 				"type": "string" 			}, 			{ 				"internalType": "string", 				"name": "_timeData", 				"type": "string" 			} 		], 		"name": "storePrediction", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string[]", 				"name": "_records", 				"type": "string[]" 			} 		], 		"name": "storeRecords", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "retrieveModels", 		"outputs": [ 			{ 				"components": [ 					{ 						"internalType": "string", 						"name": "name", 						"type": "string" 					}, 					{ 						"internalType": "string", 						"name": "hash", 						"type": "string" 					} 				], 				"internalType": "struct IA.Model[]", 				"name": "", 				"type": "tuple[]" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "retrievePredicitons", 		"outputs": [ 			{ 				"components": [ 					{ 						"internalType": "string", 						"name": "prediction", 						"type": "string" 					}, 					{ 						"internalType": "string", 						"name": "timeData", 						"type": "string" 					} 				], 				"internalType": "struct IA.Prediction[]", 				"name": "", 				"type": "tuple[]" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "retrieveRecords", 		"outputs": [ 			{ 				"internalType": "string[]", 				"name": "", 				"type": "string[]" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]')

contract = web3.eth.contract(address=contract_Address, abi=contract_abi)
nonce = web3.eth.getTransactionCount(account)

def obterRegistros():
    # Wait for transaction to be mined
    transaction = contract.functions.retrieveRecords().call()
    
    return transaction

def enviarModelo(name, hash):   
    transaction = contract.functions.storeModel(name, hash).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chain_id,
            "from": account,
            "nonce": nonce 
        }
    )
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key = private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

arq = open("/content/drive/MyDrive/IA/temp.csv","w")

for lnh in obterRegistros():
    print(lnh)
    arq.write(lnh)
    arq.write("\n")
 
arq.close()

iris = pd.read_csv("/content/drive/MyDrive/IA/temp.csv") #load the dataset

iris.head(5) #show the first 5 rows from the dataset

iris.info()  #checking if there is any inconsistency in the dataset
#as we see there are no null values in the dataset, so the data can be processed

train, test = train_test_split(iris, test_size = 0.3)# in this our main data is split into train and test
# the attribute test_size=0.3 splits the data into 70% and 30% ratio. train=70% and test=30%
print(train.shape)
print(test.shape)

train_X = train[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]# taking the training data features
train_y = train.Species# output of our training data
test_X = test[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']] # taking test data features
test_y = test.Species   #output value of test data

#Initializing the MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(100,100,100),max_iter=500)
#Fitting the training data to the network
mlp.fit(train_X, train_y)

# save the model to disk
filename = 'modeloIris.sav'
pickle.dump(mlp, open(filename, 'wb'))

# Connect to the IPFS cloud service
pinata_api_key="d84f04e5927da4e7527f"
pinata_secret_api_key="aafb51910fc9adbd15bdb884f3e2846818013381b3f040a03fcbfc2424031052" 
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

# Upload the file
result = pinata.pin_file_to_ipfs(filename)

# Should return the CID (unique identifier) of the file
print(result['IpfsHash'])  

enviarModelo("IrisModel11", result['IpfsHash'])
os.remove("/content/drive/MyDrive/IA/temp.csv")