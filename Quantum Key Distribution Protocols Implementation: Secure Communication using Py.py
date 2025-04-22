from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import random

# Generate a random bit string (sequence of '0' and '1') of a given length
def generate_bit_string(length):
    return ''.join(random.choices(['0', '1'], k=length))

# Simulate BB84 Quantum Key Distribution
def generate_quantum_key_bb84(length):
    """
    This function simulates the BB84 protocol for quantum key distribution.
    
    Parameters:
        length (int): The number of qubits to use for the protocol.
        
    Returns:
        dict: A dictionary containing the raw key, sender basis, receiver basis, and sifted key.
    """

    # Create quantum and classical registers
    qr = QuantumRegister(length, 'q')  # Quantum bits
    cr = ClassicalRegister(length, 'c')  # Classical bits for measurement
    circuit = QuantumCircuit(qr, cr)

    # Step 1: Sender (Alice) generates a random bit string (0 or 1)
    bit_string = generate_bit_string(length)

    # Step 2: Sender randomly chooses a basis (0 = standard/Z, 1 = Hadamard/X)
    basis_choices = generate_bit_string(length)

    # Step 3: Alice prepares qubits based on her bit string and basis choices
    for i in range(length):
        if bit_string[i] == '1':
            circuit.x(qr[i])  # Encode bit value 1 as |1⟩
        if basis_choices[i] == '1':
            circuit.h(qr[i])  # If using Hadamard basis, apply H gate to create superposition

    # Step 4: Receiver (Bob) randomly chooses a basis to measure each qubit
    receiver_basis = generate_bit_string(length)

    # Step 5: Bob measures each qubit in his chosen basis
    for i in range(length):
        if receiver_basis[i] == '1':
            circuit.h(qr[i])  # Apply Hadamard before measurement if using X basis
        circuit.measure(qr[i], cr[i])  # Measure qubit into classical bit

    # Step 6: Simulate the quantum circuit using QASM simulator
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1)  # Only one shot needed, as each qubit is used once
    result = job.result()
    counts = result.get_counts()
    raw_key = list(counts.keys())[0]  # Only one result due to 1 shot

    # Step 7: Compare Alice's and Bob's bases to create a sifted key
    # Only bits where both used the same basis are kept
    sifted_key = ''.join([
        raw_key[i] for i in range(length) if basis_choices[i] == receiver_basis[i]
    ])

    # Return all data for inspection
    return {
        "raw_key": raw_key,
        "basis_sender": basis_choices,
        "basis_receiver": receiver_basis,
        "sifted_key": sifted_key
    }

# Run the BB84 simulation and print results
if __name__ == "__main__":
    key_data = generate_quantum_key_bb84(16)

    print("=== BB84 Quantum Key Distribution ===")
    print("Raw Key (Bob's measurements):", key_data['raw_key'])
    print("Sender Basis (Alice):        ", key_data['basis_sender'])
    print("Receiver Basis (Bob):        ", key_data['basis_receiver'])
    print("Sifted Key (Matching Bases): ", key_data['sifted_key'])

🧠 Explanation: How BB84 Works

    Random Bit Generation (Alice):
    Alice generates a random string of bits (0 or 1).

    Random Basis Selection (Alice):
    For each bit, Alice also randomly chooses a basis:

        Z basis (standard) → measure normally.

        X basis (Hadamard) → apply Hadamard gate before measurement.

    Quantum State Preparation:
    Each qubit is encoded according to the bit value and basis:

        0 in Z → |0⟩

        1 in Z → |1⟩

        0 in X → |+⟩ (superposition)

        1 in X → |−⟩ (inverse superposition)

    Transmission and Measurement (Bob):
    Bob receives the qubits and randomly chooses his own basis to measure them. He doesn’t know Alice’s basis.

    Basis Reconciliation:
    Alice and Bob communicate publicly (e.g., over the internet) and compare their basis choices. They discard all bits where the bases were different.

    Key Extraction:
    The remaining bits (where both used the same basis) are called the sifted key and are used for encryption.

🔐 Why BB84 Is Secure

    If an eavesdropper (Eve) tries to measure the qubits, she doesn’t know the correct basis and introduces errors.

    Alice and Bob can check for these errors by revealing a small subset of their sifted key.

    If too many errors are found, they know the channel was compromised.
