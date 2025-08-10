import cirq
import numpy as np
import datetime as _dt
import hashlib as _hashlib
import json as _json
import requests

class QuantumBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.smart_contracts = {}
        self.qubits = cirq.LineQubit.range(512)
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_block = self._create_block(
            data="genesis block", proof=100, previous_hash="0", index=1
        )
        self.chain.append(genesis_block)

    def _create_block(self, data, proof, previous_hash, index):
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        
        # Create separate qubits for this block to avoid conflicts
        signature_qubits = cirq.LineQubit.range(256)
        circuit = cirq.Circuit()
        block_data = _json.dumps(block).encode()
        
        for i, byte in enumerate(block_data[:32]):  # Limit to 32 bytes to avoid qubit conflicts
            for j in range(8):
                if (byte >> j) & 1:
                    circuit.append(cirq.X(signature_qubits[i*8 + j]))
        
        # Apply quantum hash
        circuit.append(cirq.H.on_each(*signature_qubits[:256]))
        circuit.append(cirq.measure(*signature_qubits[:256], key='quantum_signature'))
        
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)
        
        block['quantum_signature'] = ''.join(map(str, result.measurements['quantum_signature'][0]))
        
        return block

    def _quantum_hash(self):
        # This method is now handled inline in _create_block
        pass

    def _simple_proof_of_work(self, previous_proof: int, index: int, data: str) -> int:
        # Simple proof of work for now
        proof = 0
        while True:
            guess = f'{previous_proof}{proof}{data}'.encode()
            guess_hash = _hashlib.sha256(guess).hexdigest()
            if guess_hash[:4] == "0000":
                break
            proof += 1
        return proof

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def mine_block(self):
        last_block = self.last_block
        last_proof = last_block['proof']
        index = len(self.chain) + 1
        data = self.current_transactions
        # Use simple proof of work for now
        proof = self._simple_proof_of_work(last_proof, index, str(data))
        previous_hash = self._hash(last_block)
        block = self._create_block(data, proof, previous_hash, index)
        
        self.current_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def _hash(block):
        block_string = _json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(block_string).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block['previous_hash'] != self._hash(previous_block):
                return False
            if not self._valid_proof(previous_block['proof'], current_block['proof'], current_block['data']):
                return False
        return True

    def _valid_proof(self, last_proof, proof, data):
        guess = f'{last_proof}{proof}{data}'.encode()
        guess_hash = _hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def get_quantum_state(self):
        qubits = cirq.LineQubit.range(10)
        circuit = cirq.Circuit(cirq.H.on_each(qubits))
        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)
        state_vector = result.final_state_vector
        return [f"{x.real}+{x.imag}j" for x in state_vector]

    # Smart contract implementation
    def create_smart_contract(self, contract_id, code):
        self.smart_contracts[contract_id] = code

    def execute_smart_contract(self, contract_id, *args):
        if contract_id not in self.smart_contracts:
            raise ValueError("Smart contract not found")
        
        contract_code = self.smart_contracts[contract_id]
        
        # Simple contract execution for demonstration
        # In a real implementation, this would parse Solidity and execute it
        if "setMessage" in contract_code and len(args) > 0:
            return f"Message set to: {args[0]}"
        elif "getMessage" in contract_code:
            return "Hello from Quanta Block!"
        elif "transfer" in contract_code and len(args) >= 3:
            return f"Transferred {args[2]} from {args[0]} to {args[1]}"
        else:
            return f"Contract executed with args: {args}"

    def _find_api_calls(self, code):
        # Simplified Grover's algorithm to find API calls in the code
        api_calls = []
        n = len(code)
        N = 2**n

        def oracle():
            circuit = cirq.Circuit()
            for i, char in enumerate(code):
                if char == 'h' and code[i:i+4] == 'http':
                    circuit.append(cirq.X(self.qubits[i]))  # Make sure indices are unique
            return circuit

        def diffusion():
            circuit = cirq.Circuit()
            circuit.append(cirq.H.on_each(*self.qubits[:n]))
            circuit.append(cirq.X.on_each(*self.qubits[:n]))
            circuit.append(cirq.H(self.qubits[n-1]))

            # Proper handling of CCX for unique qubits
            if n >= 3:
                # Apply CCX correctly across three distinct qubits
                for i in range(1, n-1):
                    circuit.append(cirq.CCX(self.qubits[i-1], self.qubits[i], self.qubits[i+1]))

            circuit.append(cirq.H(self.qubits[n-1]))
            circuit.append(cirq.X.on_each(*self.qubits[:n]))
            circuit.append(cirq.H.on_each(*self.qubits[:n]))
            return circuit

        circuit = cirq.Circuit()
        iterations = int(np.pi/4 * np.sqrt(N))
        for _ in range(iterations):
            circuit.append(oracle())
            circuit.append(diffusion())
            circuit.append(cirq.measure(*self.qubits[:n], key='api_calls'))

        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)

        for i, bit in enumerate(result.measurements['api_calls'][0]):
            if bit and code[i:i+4] == 'http':
                end = code.find('"', i)
                api_calls.append(code[i:end])

        return api_calls


# Example usage
if __name__ == "__main__":
    blockchain = QuantumBlockchain()
    
    print("Mining first block...")
    first_block = blockchain.mine_block()
    print(f"Block mined: {first_block}")
    
    print("\nAdding a transaction...")
    blockchain.add_transaction("Alice", "Bob", 50)
    
    print("\nMining second block...")
    second_block = blockchain.mine_block()
    print(f"Block mined: {second_block}")
    
    print("\nValidating blockchain...")
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")
    
    print("\nGetting quantum state...")
    quantum_state = blockchain.get_quantum_state()
    print(f"Quantum state: {quantum_state}")
    
    print("\nCreating and executing a smart contract...")
    contract_code = """
def smart_contract(x, y):
    api_response = requests.get("http://api.example.com/data").json()
    return x + y + api_response['value']
"""
    blockchain.create_smart_contract("example_contract", contract_code)
    result = blockchain.execute_smart_contract("example_contract", 5, 3)
    print(f"Smart contract result: {result}")