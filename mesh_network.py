import random
import time
from rsa_encryption import RSA

class MeshNetwork:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.messages_sent = 0
        self.total_hops = 0
        self.nodes = [RSA() for _ in range(num_nodes)]

    def send_message(self, route, encrypted_message):
        start_time = time.time()
        print(f"\nRouting message through: {route}")
        for i, node in enumerate(route[:-1]):
            self.messages_sent += 1
            self.total_hops += 1
            delay = random.uniform(0.1, 0.5)
            print(f"  Hop {i+1}: Message passed through Node {node}. Delay: {delay:.2f}s")
            time.sleep(delay)  # Simulate network delay

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Message delivered. Total time: {total_time:.2f}s")
        return total_time

    def encrypt_message(self, sender, receiver, message):
        print(f"Encrypting message from Node {sender} to Node {receiver}")
        receiver_public_key = self.nodes[receiver].get_public_key()
        return self.nodes[sender].encrypt(message, receiver_public_key)

    def decrypt_message(self, receiver, encrypted_message):
        print(f"Decrypting message at Node {receiver}")
        return self.nodes[receiver].decrypt(encrypted_message)

    def print_stats(self):
        print(f"\nNetwork Statistics:")
        print(f"Total messages sent: {self.messages_sent}")
        print(f"Total hops: {self.total_hops}")
        print(f"Average hops per message: {self.total_hops / self.messages_sent:.2f}")