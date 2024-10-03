import random
import traceback
from mesh_network import MeshNetwork
from router import Router
from blockchain import Blockchain
from huffman_coding import huffman_encode, huffman_decode

def simulate_network(num_nodes, num_messages):
    print(f"Initializing network simulation with {num_nodes} nodes and {num_messages} messages")
    network = MeshNetwork(num_nodes)
    router = Router(num_nodes)
    blockchain = Blockchain()

    for i in range(num_messages):
        try:
            print(f"\n--- Processing Message {i+1} ---")
            sender = random.randint(0, num_nodes - 1)
            receiver = random.randint(0, num_nodes - 1)
            while receiver == sender:
                receiver = random.randint(0, num_nodes - 1)

            message = f"Hello from Node {sender} to Node {receiver}"
            print(f"Original message: {message}")
            
            print("Compressing message...")
            encoded_message, codes = huffman_encode(message)
            print(f"Compressed message: {encoded_message}")
            
            print("Encrypting message...")
            encrypted_message = network.encrypt_message(sender, receiver, encoded_message)
            print("Message encrypted")
            
            print("Finding route...")
            route = router.find_route(sender, receiver)
            print(f"Route found: {route}")
            
            print("Sending message through the network...")
            actual_time = network.send_message(route, encrypted_message)
            
            print("Updating router's neural network...")
            router.update_route(route, actual_time)
            
            print("Decrypting and decompressing message at receiver...")
            decrypted_message = network.decrypt_message(receiver, encrypted_message)
            decompressed_message = huffman_decode(decrypted_message, codes)
            print(f"Received message: {decompressed_message}")
            
            print("Adding message to blockchain...")
            blockchain.add_block(f"Message from {sender} to {receiver}: {decompressed_message}")
            print("Message added to blockchain")
        
        except Exception as e:
            print(f"An error occurred while processing message {i+1}:")
            print(str(e))
            print(traceback.format_exc())
            print("Continuing with the next message...")

    print("\n--- Simulation Complete ---")
    network.print_stats()
    
    print("\nBlockchain:")
    blockchain.print_chain()

if __name__ == "__main__":
    simulate_network(num_nodes=5, num_messages=10)