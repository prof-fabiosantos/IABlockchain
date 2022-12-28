// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract IA {

     struct Prediction {
        string prediction;
        string timeData;        
    }

    string[] dataset;
    Prediction[] predictions;
    
    function storeRecords(string[] memory _records) public {
        dataset = _records;
    }
    
    function retrieveRecords() public view returns (string[] memory){
        return dataset;
    }
   
    function storePrediction(string memory _prediciton, string memory _timeData) public {
        predictions.push(Prediction(_prediciton,_timeData));
    }

    function retrievePredicitons() public view returns (Prediction[] memory){
        return predictions;
    }
        
}