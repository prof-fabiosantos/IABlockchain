
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split #to split the dataset for training and testing
from sklearn.neural_network import MLPClassifier #Importing MLPClassifier for classification.
from sklearn import metrics
import json
from web3 import Web3
import os
import calendar
import time

# add your blockchain connection information
infura_url = 'https://goerli.infura.io/v3/5ff13871021244b79ad9642b2f6499e3'
web3 = Web3(Web3.HTTPProvider(infura_url))
chain_id = 5

account = "0xc144cD60Be02F5d5C6CFfcb56DcE32D99097Afb9"
private_key = '3cd656d14571c2f3c39b97dc273060f7653ec6c2fbbb916e717b4e9f1e28f147'

#contract address and abi
contract_Address = '0x78792121DAB6cb9d68BF3354fEDD8FBC17be054d'
contract_abi = json.loads('[ 	{ 		"inputs": [], 		"name": "retrievePredicitons", 		"outputs": [ 			{ 				"components": [ 					{ 						"internalType": "string", 						"name": "prediction", 						"type": "string" 					}, 					{ 						"internalType": "string", 						"name": "timeData", 						"type": "string" 					} 				], 				"internalType": "struct IA.Prediction[]", 				"name": "", 				"type": "tuple[]" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "retrieveRecords", 		"outputs": [ 			{ 				"internalType": "string[]", 				"name": "", 				"type": "string[]" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_prediciton", 				"type": "string" 			}, 			{ 				"internalType": "string", 				"name": "_timeData", 				"type": "string" 			} 		], 		"name": "storePrediction", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string[]", 				"name": "_records", 				"type": "string[]" 			} 		], 		"name": "storeRecords", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	} ]')

contract = web3.eth.contract(address=contract_Address, abi=contract_abi)
nonce = web3.eth.getTransactionCount(account)

def obterRegistros():
    # Wait for transaction to be mined
    transaction = contract.functions.retrieveRecords().call()
    
    return transaction

def enviarPredicao(_predicao, _timestamp):   
    transaction = contract.functions.storePrediction(_predicao, _timestamp).buildTransaction(
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


arq = open("./temp.csv","w")
for lnh in obterRegistros():
    print(lnh)
    arq.write(lnh)
    arq.write("\n")
 
arq.close()

#load the dataset
iris = pd.read_csv('./temp.csv')  
iris.head(5) #show the first 5 rows from the dataset
iris.info()  #checking if there is any inconsistency in the dataset
#as we see there are no null values in the dataset, so the data can be processed

# in this our main data is split into train and test
# the attribute test_size=0.3 splits the data into 70% and 30% ratio. train=70% and test=30%
train, test = train_test_split(iris, test_size = 0.3)
print(train.shape)
print(test.shape)
# taking the training data features
train_X = train[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
# output of our training data
train_y = train.Species
# taking test data features
test_X = test[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']] 
#output value of test data
test_y = test.Species   

#Initializing the MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(100,100,100),max_iter=500)
#Fitting the training data to the network
mlp.fit(train_X, train_y)

#Predicting y for X_val
prediction = mlp.predict(test_X)

print('A acuracua do MultLayer Perceptron é ',metrics.accuracy_score(test_y,prediction))

# new data to be classified
X_new = np.array([[1, 2.9, 10, 0.2]])
prediction = mlp.predict(X_new)

import datetime;
from datetime import datetime  
  
current_time = datetime.now()  
time_stamp = current_time.timestamp()
date_time = datetime.fromtimestamp(time_stamp)
print("The date and time is:", str(date_time))

#send prediction to blockchain


if prediction[0] == 0.0:
  print('Setosa')
  enviarPredicao('Setosa', str(date_time))
elif prediction[0] == 1.0:
  print('Versicolor')
  enviarPredicao('Versicolor', str(date_time))
else:
  print('Virginica')
  enviarPredicao('Virginica', str(date_time))

os.remove('./temp.csv')