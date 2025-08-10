#!/usr/bin/env python3
"""
Test script for Quanta Block
This script demonstrates all the features of the quantum blockchain
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🚀 Quanta Block - Feature Demonstration")
    print("=" * 50)
    
    # Test 1: Get blockchain
    print("\n1. 📋 Getting current blockchain state...")
    chain = test_endpoint("/chain")
    print(f"   Blockchain length: {chain.get('length', 'N/A')}")
    print(f"   Genesis block: {chain.get('chain', [{}])[0].get('data', 'N/A')}")
    
    # Test 2: Validate blockchain
    print("\n2. ✅ Validating blockchain...")
    validation = test_endpoint("/validate")
    print(f"   Blockchain valid: {validation.get('valid', 'N/A')}")
    
    # Test 3: Get quantum state
    print("\n3. ⚛️  Getting quantum state...")
    quantum_state = test_endpoint("/quantum_state")
    state_vector = quantum_state.get('quantum_state', [])
    print(f"   Quantum state vector length: {len(state_vector)}")
    print(f"   First few states: {state_vector[:5]}")
    
    # Test 4: Add transaction
    print("\n4. 💰 Adding a transaction...")
    transaction_data = {
        "sender": "Alice",
        "recipient": "Bob", 
        "amount": 100.0
    }
    transaction = test_endpoint("/transactions/new", "POST", transaction_data)
    print(f"   Transaction result: {transaction.get('message', 'N/A')}")
    
    # Test 5: Deploy smart contract
    print("\n5. 📜 Deploying smart contract...")
    contract_data = {
        "contract_id": "TestContract",
        "contract_code": """
        pragma solidity ^0.8.0;
        contract TestContract {
            string public message;
            uint public counter;
            
            constructor() {
                message = "Hello from Quanta Block!";
                counter = 0;
            }
            
            function setMessage(string memory newMessage) public {
                message = newMessage;
                counter++;
            }
            
            function getMessage() public view returns (string memory) {
                return message;
            }
            
            function getCounter() public view returns (uint) {
                return counter;
            }
        }
        """
    }
    deployment = test_endpoint("/smart_contract/deploy", "POST", contract_data)
    print(f"   Deployment result: {deployment.get('message', 'N/A')}")
    
    # Test 6: List smart contracts
    print("\n6. 📋 Listing deployed smart contracts...")
    contracts = test_endpoint("/smart_contracts")
    print(f"   Deployed contracts: {contracts.get('smart_contracts', [])}")
    
    # Test 7: Execute smart contract
    print("\n7. ⚡ Executing smart contract...")
    execution_data = {
        "contract_id": "TestContract",
        "args": ["Updated message from Quanta Block!"]
    }
    execution = test_endpoint("/smart_contract/execute", "POST", execution_data)
    print(f"   Execution result: {execution.get('result', 'N/A')}")
    
    # Test 8: Get updated blockchain
    print("\n8. 📊 Getting updated blockchain state...")
    updated_chain = test_endpoint("/chain")
    print(f"   Updated blockchain length: {updated_chain.get('length', 'N/A')}")
    
    print("\n🎉 Quanta Block demonstration completed!")
    print(f"🌐 Server running at: {BASE_URL}")
    print("📖 Available endpoints:")
    print("   - GET  /chain - Get blockchain")
    print("   - GET  /validate - Validate blockchain")
    print("   - GET  /quantum_state - Get quantum state")
    print("   - POST /transactions/new - Add transaction")
    print("   - GET  /mine - Mine new block")
    print("   - POST /smart_contract/deploy - Deploy contract")
    print("   - POST /smart_contract/execute - Execute contract")
    print("   - GET  /smart_contracts - List contracts")

if __name__ == "__main__":
    main()
