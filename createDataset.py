
import json
from web3 import Web3

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

def enviarRegistros(comando):   
    transaction = contract.functions.storeRecords(comando).buildTransaction(
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

# Criando o array do dataset
dataset = []

arq = open("iris.csv")
registros = arq.readlines()
for registro in registros:
    print(registro)
    dataset.append(registro)

enviarRegistros(dataset)



